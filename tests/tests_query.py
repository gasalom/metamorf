from metamorf.tools.query import *
import metamorf.tools.metadata
from metamorf.constants import *
'''
query = metamorf.tools.query.Query()
query.set_name_query('EJEMPLO')
query.set_is_with(False)
query.set_is_distinct(True)
query.set_select_columns(['ID', 'NAME'])
query.set_type(QUERY_TYPE_SELECT)
query.set_insert_columns(['ID', 'NAME'])
#query.setFromTables(['PRUEBA'])
query.set_from_tables_and_relations([metamorf.FromRelationQuery('A', 'ID', 'B', 'ID', 0, "="), metamorf.FromRelationQuery('D', 'ID', 'C', 'ID', 1, "=") , metamorf.tools.query.FromRelationQuery('B', 'ID', 'C', 'ID', 2, "=")])
query.set_where_filters(['ID > 0'])
#query.setHavingFilters(['count(1)>1'])
query.set_group_by_columns(['ID', 'NAME'])
query.set_order_by_columns([metamorf.OrderByQuery('ID', 'asc') , metamorf.OrderByQuery('NAME', 'desc')])

queryWithA = metamorf.tools.query.Query()
queryWithA.set_name_query("A")
queryWithA.set_is_with(True)
queryWithA.set_select_columns(['ID'])
queryWithA.set_from_tables(['Z'])

queryWithOrigen = metamorf.tools.query.Query()
queryWithOrigen.set_name_query("Z")
queryWithOrigen.set_is_with(True)
queryWithOrigen.set_select_columns(['ID_2 as ID', 'FECHA'])
queryWithOrigen.set_from_tables(['ORIGEN'])
queryWithOrigen.set_where_filters(['FECHA>SYSDATE'])

query.add_subquery(queryWithA)
query.add_subquery(queryWithOrigen)

queryUnion = metamorf.tools.query.Query()
queryUnion.set_name_query('EJEMPLO')
queryUnion.set_is_with(False)
queryUnion.set_is_distinct(True)
queryUnion.set_select_columns(['FUNCIONA.ID', 'FUNCIONA.NAME'])
queryUnion.set_type(QUERY_TYPE_SELECT)
queryUnion.set_insert_columns(['ID', 'NAME'])
queryUnion.set_from_tables(["FUNCIONA"])

query.add_unionquery(queryUnion)

#print(str(query))
'''

queryValues = metamorf.tools.query.Query()
queryValues.set_has_header(True)
queryValues.set_type(QUERY_TYPE_VALUES)
queryValues.set_name_query('ENTRY_AGGREGATORS')
queryValues.set_insert_columns(COLUMNS_ENTRY_AGGREGATORS)

metadata = metamorf.tools.metadata.Metadata()
metadata.add_entry_aggregators([['COD_ENTITY_TARGET', 'COD_ENTITY_SOURCE', 'COLUMN_NAME', 'NUM_BRANCH'], ['TARGET', 'SRC','ID','1'], ['TARGETO', 'SRC', 'NAME', '2']])

queryValues.set_values(metadata.entry_aggregators)

print(str(queryValues))





