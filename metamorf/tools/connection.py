from abc import ABC, abstractmethod
import sqlite3
import snowflake.connector
import mysql.connector
from metamorf.constants import *
import hashlib
import fdb
import psycopg2
from metamorf.tools.log import Log
from metamorf.tools.database_objects import Column

class Connection(ABC):

    def __init__(self):
        self.conn = None
        self.is_executing = False
        self.engine_name = "Connection"

    def setup_connection(self, configuration: dict, log: Log):
        self.log = log
        self.get_connection(configuration)
        self._get_cursor()
        self.setup_after_connection_established()

    @abstractmethod
    def get_connection(self, configuration: dict):
        pass

    @abstractmethod
    def get_connection_type(self):
        pass

    @abstractmethod
    def get_sysdate_value(self):
        pass

    @abstractmethod
    def get_sysdate_value_infinite(self):
        pass

    @abstractmethod
    def get_table_columns_definition(self, table_name):
        pass

    @abstractmethod
    def does_table_exists(self, table_name):
        pass

    def setup_after_connection_established(self):
        pass

    def _get_cursor(self):
        if self.conn is None:
            self.cursor = None
        else:
            self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def execute(self, all_queries: str):
        """Return a boolean with the result of the execution."""
        self.is_executing = True
        if self.cursor is None:
            self.log.log(self.engine_name, 'The connection is not prepared to execute', LOG_LEVEL_ERROR)
            self.is_executing = False
            return False


        if len(all_queries) == 0:
            self.log.log(self.engine_name, 'There\'s nothing to load', LOG_LEVEL_ONLY_LOG)
            return True
        queries = all_queries.split(";")
        num_queries = len(queries)
        if queries[-1] == "": num_queries -= 1
        if num_queries==1: self.log.log(self.engine_name, "Starting to execute " + str(num_queries) + " query", LOG_LEVEL_ONLY_LOG)
        if num_queries > 1: self.log.log(self.engine_name, "Starting to execute " + str(num_queries) + " queries", LOG_LEVEL_ONLY_LOG)

        num_queries_executed = 0
        for q in queries:
            if q is None or q.strip() == '':
                continue
            try:
                q = q.strip()
                self.cursor.execute(q)
                self.log.log(self.engine_name, "Query Executed:\n" + q, LOG_LEVEL_ONLY_LOG)
                num_queries_executed += 1
            except Exception as e:
                self.log.log(self.engine_name, "Query Executed:\n" + q, LOG_LEVEL_ONLY_LOG)
                self.log.log(self.engine_name, "Error: " + str(e), LOG_LEVEL_ERROR)
                self.is_executing = False
                return False
            #if(self.connection_type == CONNECTION_FIREBIRD): self.connection.commit()
        if num_queries == 1: self.log.log(self.engine_name, "Query Finished Ok", LOG_LEVEL_ONLY_LOG)
        if num_queries > 1: self.log.log(self.engine_name, "All queries finished Ok", LOG_LEVEL_ONLY_LOG)
        self.is_executing = False
        return True

    def get_query_result(self):
        return self.cursor.fetchall()

    def get_md5_function(self):
        return "MD5([x])"

    @abstractmethod
    def get_hash_for_metadata(self):
        pass

    @abstractmethod
    def get_sysdate_for_metadata(self):
        pass

    @abstractmethod
    def get_cast_string_for_metadata(self):
        pass

    @abstractmethod
    def get_integer_for_metadata(self):
        pass

    @abstractmethod
    def get_string_for_metadata(self):
        pass


class ConnectionSQLite(Connection):
    def get_connection_type(self):
        return CONNECTION_SQLITE

    def get_connection(self, configuration: dict):
        self.log.log(self.engine_name, "Trying to connect to the SQLite database", LOG_LEVEL_ONLY_LOG)
        self.conn = sqlite3.connect(configuration['sqlite_path'])
        sqlite3.enable_callback_tracebacks(True)
        self.log.log(self.engine_name, "Connection to the SQLite database established", LOG_LEVEL_ONLY_LOG)

    # Usage on the SQLITE connection because hashing functions doesn't exist on this db
    def _md5(self,word):
        final_word = str(word)
        return hashlib.md5(final_word.encode('utf-8')).hexdigest()

    def setup_after_connection_established(self):
        self.log.log(self.engine_name, "Adding MD5 Function to the SQLite Database", LOG_LEVEL_ONLY_LOG)
        self.conn.create_function("MD5", 1, self._md5)
        self.log.log(self.engine_name, "Added MD5 Function to the SQLite Database", LOG_LEVEL_ONLY_LOG)

    def get_sysdate_value(self):
        return 'datetime(\'now\')'

    def get_sysdate_value_infinite(self):
        return "DATETIME(\'9999-12-31 00:00:00\')"

    def get_table_columns_definition(self, table_name):
        query_to_execute = "PRAGMA TABLE_INFO(" + table_name + ")"
        self.execute(query_to_execute)
        result = self.get_query_result()
        all_columns = []
        for r in result:
            if r[3] == 1: is_nullable = 1
            else: is_nullable = 0
            pk_result = "NULL"
            if r[5] == 1: pk_result="PK"
            all_columns.append(Column(r[0], r[1], r[2], r[4], pk_result, is_nullable,0,0,0))
        return all_columns

    def does_table_exists(self, table_name):
        query_to_execute = "PRAGMA TABLE_INFO(" + table_name + ")"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result)>0: return True
        return False

    def get_hash_for_metadata(self):
        return ['TEXT', 0, 0]

    def get_sysdate_for_metadata(self):
        return ['TEXT', 0, 0]

    def get_cast_string_for_metadata(self):
        return 'CAST([x] as text)'

    def get_integer_for_metadata(self):
        return ['INTEGER', 0, 0]

    def get_string_for_metadata(self):
        return ['TEXT', 0, 0]

class ConnectionMySQL(Connection):
    def get_connection_type(self):
        return CONNECTION_MYSQL

    def get_connection(self, configuration: dict):
        self.log.log(self.engine_name, "Trying to connect to the MySQL database", LOG_LEVEL_ONLY_LOG)

        self.conn = mysql.connector.connect(
            user = configuration['mysql_user'],
            password = configuration['mysql_password'],
            host = configuration['mysql_host'],
            database = configuration['mysql_database']
        )
        self.log.log(self.engine_name, "Finished to connect to the MySQL database", LOG_LEVEL_ONLY_LOG)

    def setup_after_connection_established(self):
        self.activate_concate_with_pipes()

    def activate_concate_with_pipes(self):
        self.log.log(self.engine_name, "Activating concat by pipes", LOG_LEVEL_ONLY_LOG)
        set_on_concat_by_pipes = "SET sql_mode=(SELECT CONCAT(@@sql_mode,',PIPES_AS_CONCAT')) "
        self.execute(set_on_concat_by_pipes)
        self.log.log(self.engine_name, "Activation finished", LOG_LEVEL_ONLY_LOG)

    def get_sysdate_value(self):
        return 'CURRENT_TIMESTAMP()'

    def get_sysdate_value_infinite(self):
        return "TIMESTAMP(\'9999-12-31 00:00:00\')"

    def get_table_columns_definition(self, table_name):
        # ID, COLUMN NAME, TYPE, DEFAULT_VALUE, PK 0/1, IS_NULLABLE, LENGTH, PRECISION, SCALE
        query_to_execute =  "select ordinal_position, column_name, data_type, COLUMN_DEFAULT, COLUMN_KEY, is_nullable, character_maximum_length, numeric_precision, numeric_scale " +\
                            " FROM information_schema.columns " +\
                            " WHERE table_name = '"+table_name+"' "
        self.execute(query_to_execute)
        result = self.get_query_result()
        all_columns = []
        for r in result:
            if r[5] == 'YES':
                is_nullable = 1
            else:
                is_nullable = 0
            if r[6] is None: length = 0
            else: length = r[6]
            if r[7] is None: precision = 0
            else: precision = r[7]
            if r[8] is None: scale = 0
            else: scale = r[8]
            pk_result = "NULL"
            if r[4] == "PRI": pk_result="PK"
            #                         id, name, type, default, is_pk, is_nullable, length, precision, scale
            all_columns.append(Column(r[0], r[1], r[2], r[3], pk_result, is_nullable, length, precision, scale))
        return all_columns

    def does_table_exists(self, table_name):
        query_to_execute = "select column_name FROM information_schema.columns WHERE table_name = '" + table_name + "'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result) > 0: return True
        return False

    def get_hash_for_metadata(self):
        return ['BINARY', 32, 0]

    def get_sysdate_for_metadata(self):
        return ['DATETIME', 0, 0]

    def get_cast_string_for_metadata(self):
        return 'CAST([x] as CHAR)'

    def get_integer_for_metadata(self):
        return ['INTEGER', 0, 0]

    def get_string_for_metadata(self):
        return ['VARCHAR', 0, 0]


class ConnectionPostgreSQL(Connection):
    def get_connection_type(self):
        return CONNECTION_POSTGRESQL

    def get_connection(self, configuration: dict):
        self.log.log(self.engine_name, "Trying to connect to the PostgreSQL database", LOG_LEVEL_ONLY_LOG)
        self.conn = psycopg2.connect(
            user = configuration['postgres_user'],
            password = configuration['postgres_password'],
            host = configuration['postgres_host'],
            database = configuration['postgres_database'],
            options= '-c search_path='+configuration['postgres_schema']
        )
        self.log.log(self.engine_name, "Finished to connect to the PostgreSQL database", LOG_LEVEL_ONLY_LOG)

    def get_sysdate_value(self):
        return 'CURRENT_TIMESTAMP'

    def get_sysdate_value_infinite(self):
        return "TO_TIMESTAMP(\'9999-12-31 00:00:00\', \'YYYY-MM-DD HH24:MI:SS\')"

    def get_table_columns_definition(self, table_name):
        table_name = table_name.lower()
        # ID, COLUMN NAME, TYPE, DEFAULT_VALUE, PK 0/1, IS_NULLABLE, LENGTH, PRECISION, SCALE
        query_to_execute =  "SELECT  ordinal_position, column_name, udt_name, column_default, 0 as is_pk, is_nullable, character_maximum_length , numeric_precision , numeric_scale " +\
                            "FROM information_schema.columns " +\
                            "WHERE  table_name = '" + table_name + "'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        all_columns = []
        for r in result:
            if r[5] == 'YES':
                is_nullable = 1
            else:
                is_nullable = 0
            if r[6] is None: length = 0
            else: length = r[6]
            if r[7] is None: precision = 0
            else: precision = r[7]
            if r[8] is None: scale = 0
            else: scale = r[8]
            pk_result = "NULL"
            if r[4] == "PRI": pk_result="PK"
            #                         id, name, type, default, is_pk, is_nullable, length, precision, scale
            all_columns.append(Column(r[0], r[1].upper(), r[2].upper(), r[3], pk_result, is_nullable, length, precision, scale))
        return all_columns

    def does_table_exists(self, table_name):
        table_name = table_name.lower()
        query_to_execute = "select column_name FROM information_schema.columns WHERE table_name = '" + table_name + "'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result) > 0: return True
        return False

    def get_hash_for_metadata(self):
        return ['TEXT', 0, 0]

    def get_sysdate_for_metadata(self):
        return ['TIMESTAMP', 0, 0]

    def get_cast_string_for_metadata(self):
        return 'CAST([x] as text)'

    def get_integer_for_metadata(self):
        return ['INTEGER', 0, 0]

    def get_string_for_metadata(self):
        return ['VARCHAR', 0, 0]


class ConnectionFirebird(Connection):
    def get_connection_type(self):
        return CONNECTION_FIREBIRD

    def get_connection(self, configuration: dict):
        self.conn = fdb.connect(
            host=configuration['firebird_host'],
            database=configuration['firebird_database'],
            user=configuration['firebird_user'],
            password=configuration['firebird_password']
        )


class ConnectionSnowflake(Connection):
    def get_connection_type(self):
        return CONNECTION_SNOWFLAKE

    def get_connection(self, configuration: dict):
        self.log.log(self.engine_name, "Trying to connect to the Snowflake database", LOG_LEVEL_ONLY_LOG)
        self.schema_connection = configuration['snowflake_schema']
        try:
            self.conn = snowflake.connector.connect(
                user = configuration['snowflake_user'],
                password = configuration['snowflake_password'],
                account = configuration['snowflake_account'],
                warehouse = configuration['snowflake_warehouse'],
                database = configuration['snowflake_database'],
                schema = configuration['snowflake_schema'],
                role = configuration['snowflake_role'],
                autocommit = False
            )
            self.log.log(self.engine_name, "Trying to connect the Snowflake database finished", LOG_LEVEL_ONLY_LOG)
        except Exception as e:
            self.log.log(self.engine_name, "Trying to connect the Snowflake database finished", LOG_LEVEL_ONLY_LOG)
            self.log.log(self.engine_name, str(e), LOG_LEVEL_ERROR)

    def get_table_columns_definition(self, table_name):
        # ID, COLUMN NAME, TYPE, DEFAULT_VALUE, PK 0/1, IS_NULLABLE, LENGTH, PRECISION, SCALE
        query_to_execute = "select ORDINAL_POSITION, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, 0 as IS_PK, "+\
                           " CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE "+\
                           " from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='"+table_name+"' and TABLE_SCHEMA = '"+self.schema_connection+"'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        all_columns = []
        for r in result:
            if r[3]=='YES': is_nullable = 1
            else: is_nullable = 0
            if r[6] is None: length = 0
            else: length = r[6]
            if r[7] is None: precision = 0
            else: precision = r[7]
            if r[8] is None: scale = 0
            else: scale = r[8]
            pk_result = "NULL"
            if r[5] == 1: pk_result="PK"
            #                         id, name, type, default, is_pk, is_nullable, length, precision, scale
            all_columns.append(Column(r[0], r[1], r[2], r[4], pk_result, is_nullable, length, precision, scale))
        return all_columns

    def does_table_exists(self, table_name):
        query_to_execute = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='" + table_name + "'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result) > 0: return True
        return False

    def get_sysdate_value(self):
        return 'CURRENT_TIMESTAMP()'

    def get_sysdate_value_infinite(self):
        return "TO_TIMESTAMP(\'9999-12-31 00:00:00\', \'YYYY-MM-DD HH24:MI:SS\')"

    def get_hash_for_metadata(self):
        return ['VARCHAR', 0, 0]

    def get_sysdate_for_metadata(self):
        return ['TIMESTAMP', 0, 0]

    def get_cast_string_for_metadata(self):
        return 'TO_CHAR([x])'

    def get_integer_for_metadata(self):
        return ['NUMBER', 0, 0]

    def get_string_for_metadata(self):
        return ['VARCHAR', 0, 0]


#####################################################################################

class ConnectionFactory:
    def get_connection(self, name_connection: str):
        if name_connection.upper() == CONNECTION_SNOWFLAKE.upper():
            return ConnectionSnowflake()
        elif name_connection.upper() == CONNECTION_SQLITE.upper():
            return ConnectionSQLite()
        elif name_connection.upper() == CONNECTION_FIREBIRD.upper():
            return ConnectionFirebird()
        elif name_connection.upper() == CONNECTION_MYSQL.upper():
            return ConnectionMySQL()
        elif name_connection.upper() == CONNECTION_POSTGRESQL.upper():
            return ConnectionPostgreSQL()
        else:
            return None

