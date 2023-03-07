from metamorf.tools.connection import ConnectionFactory, Connection
from metamorf.constants import *
from metamorf.tools.filecontroller import *
from metamorf.tools.log import *
from metamorf.tools.database_objects import *


class Test:

    def run(self):
        file_controller_configuration = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_configuration.set_file_location(ACTUAL_PATH, CONFIGURATION_FILE_NAME)
        self.configuration_file = file_controller_configuration.read_file()

        log = Log()
        self.connection = ConnectionFactory().get_connection(CONNECTION_SQLITE)
        self.connection.setup_connection(self.configuration_file['metadata'], log)

        query_create_table = "CREATE TABLE EJEMPLO(ID integer, NAME text, FECHA date)"
        #self.connection.execute(query_create_table)

        query_insert_into = "INSERT INTO ejemplo(id,name,fecha) values(?,?,?)"
        values = (1,'Aumatell, Guillermo', '2023-01-29')

        query_insert_into_total = "INSERT INTO ejemplo(id,name,fecha) values(2,'Arbona, Emma','2023-01-29')"
        self.connection.execute(query_insert_into_total)
        rows = self.connection.get_query_result()
        print(rows)

        select_query = "SELECT ID,NAME,FECHA FROM EJEMPLO"
        self.connection.execute(select_query)
        rows = self.connection.get_query_result()
        print(rows)
        for r in rows:
            print(type(r))

        #self.connection.cursor.execute(query_insert_into, values)
        #self.connection.execute(query_insert_into_total)
        #self.connection.commit()



        log.close()

#test = Test().run()
print(False and True)
print(False and False)
print(True and True)
print(False and False)

'''
om_eo = EntryOrder('EJEMPLO', 'ID', 'desc')
        print(om_eo)
        om_ea = EntryAggregators('A','B', 'ID',2)
        print(om_ea)
        om_ef = EntryFilters('A','a=1',1)
        print(om_ef)
        om_er = EntryDatasetRelationships('A','a','B','b', 'master join')
        print(om_er)
        om_ee = EntryEntity('entity' ,'A', 'TMP', 'path')
        print(om_ee)
        om_ep = EntryPath('COD_PATH','DATABASE', 'SCHEMA')
        print(om_ep)
        om_ep = EntryPath('COD_PATH', '', '')
        print(om_ep)
        om_ep = EntryPath(cod_path='COD_PATH', database_name=None, schema_name=None)
        print(om_ep)
        om_edm = EntryDatasetMappings('ENTITY_SOURCE','SUBSTR(CAMPO_A)','ENTITY_TARGET', 'CAMPO_A_GUAY','VARCHAR', 1,'PK',0)
        print(om_edm)
        om_edm = EntryDatasetMappings('ENTITY_SOURCE', 'SUBSTR(CAMPO_A)', 'ENTITY_TARGET', 'CAMPO_A_GUAY', 'VARCHAR', 1, None, 0)
        print(om_edm)
        '''