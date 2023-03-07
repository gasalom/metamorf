from abc import ABC, abstractmethod
import sqlite3
import snowflake.connector
from metamorf.constants import *
import hashlib
import fdb
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
    def get_table_columns_definition(self, table_name):
        pass

    @abstractmethod
    def does_table_exists(self, table_name):
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
            self.log.log(self.engine_name, 'There\'s nothing to load', LOG_LEVEL_DEBUG)
            return True
        queries = all_queries.split(";")
        num_queries = len(queries)
        if queries[-1] == "": num_queries -= 1
        if num_queries==1: self.log.log(self.engine_name, "Starting to execute " + str(num_queries) + " query", LOG_LEVEL_DEBUG)
        if num_queries > 1: self.log.log(self.engine_name, "Starting to execute " + str(num_queries) + " queries", LOG_LEVEL_DEBUG)

        num_queries_executed = 0
        for q in queries:
            if q is None or q == "":
                continue
            try:
                self.cursor.execute(q)
                self.log.log(self.engine_name, "Query Executed:\n" + q, LOG_LEVEL_ONLY_LOG)
                num_queries_executed += 1
            except Exception as e:
                self.log.log(self.engine_name, "Query Executed:\n" + q, LOG_LEVEL_ONLY_LOG)
                self.log.log(self.engine_name, "Error: " + str(e), LOG_LEVEL_ERROR)
                self.is_executing = False
                return False
            #if(self.connection_type == CONNECTION_FIREBIRD): self.connection.commit()
        if num_queries == 1: self.log.log(self.engine_name, "Query Finished Ok", LOG_LEVEL_OK)
        if num_queries > 1: self.log.log(self.engine_name, "All queries finished Ok", LOG_LEVEL_OK)
        self.is_executing = False
        return True

    def get_query_result(self):
        return self.cursor.fetchall()


class ConnectionSQLite(Connection):
    def get_connection_type(self):
        return CONNECTION_SQLITE

    def get_connection(self, configuration: dict):
        self.log.log(self.engine_name, "Trying to connect to the SQLite database", LOG_LEVEL_DEBUG)
        self.conn = sqlite3.connect(configuration['sqlite_path'])
        sqlite3.enable_callback_tracebacks(True)
        self.log.log(self.engine_name, "Connection to the SQLite database established", LOG_LEVEL_DEBUG)
        self.log.log(self.engine_name, "Adding MD5 Function to the SQLite Database", LOG_LEVEL_DEBUG)
        self.conn.create_function("MD5", 1, self._md5)
        self.log.log(self.engine_name, "Added MD5 Function to the SQLite Database", LOG_LEVEL_DEBUG)

    # Usage on the SQLITE connection because hashing functions doesn't exist on this db
    def _md5(self,word):
        final_word = str(word)
        return hashlib.md5(final_word.encode('utf-8')).hexdigest()

    def get_sysdate_value(self):
        return 'datetime(\'now\')'

    def get_table_columns_definition(self, table_name):
        query_to_execute = "PRAGMA TABLE_INFO(" + table_name + ")"
        self.execute(query_to_execute)
        result = self.get_query_result()
        all_columns = []
        for r in result:
            if r[3] == 1: is_nullable = 1
            else: is_nullable = 0
            all_columns.append(Column(r[0], r[1], r[2], r[4], r[5], is_nullable,0,0,0))
        return all_columns

    def does_table_exists(self, table_name):
        query_to_execute = "PRAGMA TABLE_INFO(" + table_name + ")"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result)>0: return True
        return False



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
        self.log.log(self.engine_name, "Trying to connect to the Snowflake database", LOG_LEVEL_DEBUG)
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
            self.log.log(self.engine_name, "Trying to connect the Snowflake database finished", LOG_LEVEL_DEBUG)
        except Exception as e:
            self.log.log(self.engine_name, "Trying to connect the Snowflake database finished", LOG_LEVEL_DEBUG)
            self.log.log(self.engine_name, str(e), LOG_LEVEL_ERROR)

    def get_sysdate_value(self):
        return 'CURRENT_TIMESTAMP()'

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
            #                         id, name, type, default, is_pk, is_nullable, length, precision, scale
            all_columns.append(Column(r[0], r[1], r[2], r[4], r[5], is_nullable, length, precision, scale))
        return all_columns

    def does_table_exists(self, table_name):
        query_to_execute = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='" + table_name + "'"
        self.execute(query_to_execute)
        result = self.get_query_result()
        if len(result) > 0: return True
        return False

#####################################################################################

class ConnectionFactory:
    def get_connection(self, name_connection: str):
        if name_connection.upper() == CONNECTION_SNOWFLAKE.upper():
            return ConnectionSnowflake()
        elif name_connection.upper() == CONNECTION_SQLITE.upper():
            return ConnectionSQLite()
        elif name_connection.upper() == CONNECTION_FIREBIRD.upper():
            return ConnectionFirebird()
        else:
            return None

