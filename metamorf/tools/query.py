from __future__ import annotations
from metamorf.constants import *

class Query:

    def __init__(self):
        self.type = None
        self.name_query = ""
        self.target_table = ""
        self.is_with = False
        self.is_distinct = False
        self.insert_columns = []
        self.select_columns = []
        self.from_tables = []
        self.from_tables_and_relations = []  # FromRelationQuery Class
        self.group_by_columns = []
        self.having_filters = []
        self.order_by_columns = []  # OrderByQuery Class
        self.where_filters = []
        self.primary_key = []
        self.subqueries = []  # Query Class => With
        self.union_query = [] # Query Class and only need to be settet as SELECT Statement, WITH statements need to be setted on the main Query.
        self.values = []
        self.has_header = False
        self.values_batch = 1000 # Num of values that an insert can execute
        self.columns_and_specs = []
        self.database = None
        self.is_truncate = False
        self.need_create_table = False
        self.need_drop_table = False

    def set_database(self, database: str):
        '''Set the Target database of the query. Use the constants CONNECTION_[X]'''
        self.database = database

    def set_need_create_table(self, option):
        self.need_create_table = option

    def set_need_drop_table(self, option):
        self.need_drop_table = option

    def set_is_truncate(self, is_truncate):
        self.is_truncate = is_truncate

    def set_type(self, type: int):
        self.type = type

    def set_values_batch(self, values_batch: int):
        self.values_batch = values_batch

    def set_columns_and_specs(self, columns_and_specs: []):
        self.columns_and_specs = columns_and_specs

    def add_column_and_spec(self, column_and_spec: []):
        self.columns_and_specs.append(column_and_spec)

    def set_name_query(self, name_query: str):
        self.name_query = name_query

    def set_target_table(self, target_table: str):
        self.target_table = target_table

    def set_is_with(self, option: bool):
        self.is_with = option

    def set_is_distinct(self, option: bool):
        self.is_distinct = option

    def set_select_columns(self, select_columns: list):
        self.select_columns = select_columns

    def add_select_columns(self, select_column: str):
        self.select_columns.append(select_column)

    def set_insert_columns(self, insert_columns: list):
        self.insert_columns = insert_columns

    def add_insert_columns(self, column: str):
        self.insert_columns.append(column)

    def set_from_tables(self, from_tables: list):
        if isinstance(from_tables, str):
            from_tables = [from_tables]
        self.from_tables = from_tables

    def set_from_tables_and_relations(self, from_tables_and_relations: list):
        for from_table in from_tables_and_relations:
            if not isinstance(from_table, FromRelationQuery): raise TypeError("FromRelationQuery must be set to an FromRelationQuery Object")
        self.from_tables_and_relations = from_tables_and_relations

    def set_group_by_columns(self, group_by_columns: list):
        self.group_by_columns = group_by_columns

    def set_having_filters(self, having_filters: list):
        self.having_filters = having_filters

    def set_order_by_columns(self, order_by_columns: list):
        for order in order_by_columns:
            if not isinstance(order, OrderByQuery): raise TypeError("OrderColumns must be set to an OrderByQuery Object")
        self.order_by_columns = order_by_columns

    def add_order_by_columns(self, order_by_column):
        if not isinstance(order_by_column, OrderByQuery): raise TypeError("OrderColumns must be set to an OrderByQuery Object")
        self.order_by_columns.append(order_by_column)

    def add_subquery(self, subquery: Query):
        if not isinstance(subquery, Query): raise TypeError("Subqueries must be set to a Query Object")
        self.subqueries.append(subquery)

    def add_unionquery(self, union_query: Query):
        if not isinstance(union_query, Query): raise TypeError("Unionquery must be set to a Query Object")
        self.union_query.append(union_query)

    def set_primary_key(self, primary_key: list):
        self.primary_key = primary_key

    def set_where_filters(self, where_filters: list):
        if isinstance(where_filters, str):
            where_filters = [where_filters]
        if where_filters is None:
            where_filters = []
        self.where_filters = where_filters

    def set_values(self, values: list):
        self.values = values

    def set_has_header(self, option: bool):
        self.has_header = option

    def get_dataset_name_from_fqdn(self, dataset_name):
        dataset = dataset_name.split(".")
        return dataset[len(dataset)-1]

    def _get_all_from_tables_from_query(self, query: Query):
        all_from_tables = []
        for x in query.from_tables:
            if x not in all_from_tables: all_from_tables.append(x)
        for x in query.from_tables_and_relations:
            if x.master_table not in all_from_tables: all_from_tables.append(x.master_table)
            if x.detail_table not in all_from_tables: all_from_tables.append(x.detail_table)
        return all_from_tables

    def __str__(self):
        query = ""
        all_from_tables = ""
        all_group_by_columns = ""
        all_having_columns = ""
        all_select_columns = ""
        all_insert_columns = ""
        all_where_filters = ""
        all_order_by = ""
        all_values = ""

        self.validate_query_elements()

        # Order WITH queries
        all_with_queries = self.subqueries.copy()
        all_with_to_be_processed = [] # all with that need to be processed
        for q in self.subqueries:
            if q.name_query not in all_with_to_be_processed: all_with_to_be_processed.append(q.name_query)
        all_with_to_be_processed = set(all_with_to_be_processed)
        index = 0
        all_with_ordered = [] # all_query_objects ordered
        with_added = [] # all with names that have been already added
        while all_with_queries:
            with_query = all_with_queries[index]
            all_from_tab = self._get_all_from_tables_from_query(with_query)
            for with_processed in with_added:
                if with_processed in all_from_tab: all_from_tab.remove(with_processed)
            set_all_from_tables = set(all_from_tab)
            result_intersection = list(set_all_from_tables.intersection(all_with_to_be_processed))
            if len(result_intersection)==0:
                all_with_ordered.append(with_query)
                with_added.append(with_query.name_query)
                all_with_queries.remove(with_query)
                index = 0
            else:
                index +=1

        self.subqueries = all_with_ordered.copy()
        self.subqueries.reverse()

        # SELECT
        all_select_columns += ','.join([str(col) for col in self.select_columns])

        # INSERT
        all_insert_columns += ','.join([str(col) for col in self.insert_columns])

        # FROM
        for table in self.from_tables:
            all_from_tables += table +" "+ self.get_dataset_name_from_fqdn(table) + " , "
        all_from_tables = all_from_tables[:-3]

        if len(self.from_tables) > 0: all_from_tables += ","
        includedTables = []
        all_relation_to_include = self.from_tables_and_relations
        pos = 0

        while len(all_relation_to_include) > 0:
            relation = all_relation_to_include[pos]
            if not includedTables: # If it's the first relation, we include it
                all_relations_same_tables = []
                relations_to_delete = []
                for rel in all_relation_to_include:
                    if relation.master_table == rel.master_table and relation.detail_table == rel.detail_table:
                        if rel != relation: relations_to_delete.append(rel)
                        all_relations_same_tables.append(rel)
                for rel in relations_to_delete: all_relation_to_include.remove(rel)

                all_from_tables += relation.master_table + " "+ self.get_dataset_name_from_fqdn(relation.master_table) + " " + self.get_join_from_id(relation.join_type) + " " + relation.detail_table + " " + self.get_dataset_name_from_fqdn(relation.detail_table) + " ON "

                for rel in all_relations_same_tables:
                    all_from_tables += self.get_dataset_name_from_fqdn(rel.master_table) + "." + rel.master_column + " " + rel.join_sign + " " + self.get_dataset_name_from_fqdn(rel.detail_table) + "." + rel.detail_column + " AND "

                all_from_tables = all_from_tables[:-4] + "\n"
                includedTables.append(relation.master_table)
                includedTables.append(relation.detail_table)
                all_relation_to_include.remove(relation)
                pos = 0
                continue
            else:

                if relation.master_table in includedTables:
                    all_relations_same_tables = []
                    relations_to_delete = []
                    for rel in all_relation_to_include:
                        if relation.master_table == rel.master_table and relation.detail_table == rel.detail_table:
                            if rel != relation: relations_to_delete.append(rel)
                            all_relations_same_tables.append(rel)
                    for rel in relations_to_delete: all_relation_to_include.remove(rel)

                    all_from_tables += self.get_join_from_id(relation.join_type) + " " + relation.detail_table + " " + self.get_dataset_name_from_fqdn(relation.detail_table) + " ON "
                    for rel in all_relations_same_tables:
                        all_from_tables += self.get_dataset_name_from_fqdn(rel.master_table) + "." + rel.master_column + " " + rel.join_sign + " " + self.get_dataset_name_from_fqdn(rel.detail_table) + "." + rel.detail_column + " AND "
                    all_from_tables = all_from_tables[:-4] + "\n"

                    includedTables.append(relation.detail_table)
                    all_relation_to_include.remove(relation)
                    pos = 0
                    continue
                if relation.detail_table in includedTables:

                    if relation.join_type == 1: joinType = 2
                    elif relation.join_type == 2: joinType = 1
                    else: joinType = relation.join_type

                    all_relations_same_tables = []
                    relations_to_delete = []
                    for rel in all_relation_to_include:
                        if relation.master_table == rel.master_table and relation.detail_table == rel.detail_table:
                            if rel != relation: relations_to_delete.append(rel)
                            all_relations_same_tables.append(rel)
                    for rel in relations_to_delete: all_relation_to_include.remove(rel)

                    all_from_tables += self.get_join_from_id(joinType) + " " + relation.master_table + " " + self.get_dataset_name_from_fqdn(relation.master_table)+ " ON "
                    for rel in all_relations_same_tables:
                        all_from_tables += self.get_dataset_name_from_fqdn(rel.detail_table) + "." + rel.detail_column + " " + rel.join_sign + " " + self.get_dataset_name_from_fqdn(rel.master_table) + "." + rel.master_column + " AND "
                    all_from_tables = all_from_tables[:-4] + "\n"

                    includedTables.append(relation.master_table)
                    all_relation_to_include.remove(relation)
                    pos = 0
                    continue
            pos += 1

        # delete \n
        all_from_tables = all_from_tables[:-1]

        # WHERE
        for where_filter in self.where_filters:
            all_where_filters += where_filter + " AND "
        all_where_filters = all_where_filters[:-4]

        # HAVING
        for having in self.having_filters:
            all_having_columns += having + " AND "
        all_having_columns = all_having_columns[:-4]

        # GROUP BY
        for col in self.group_by_columns:
            all_group_by_columns += col + " , "
        all_group_by_columns = all_group_by_columns[:-3]

        # ORDER BY
        for col in self.order_by_columns:
            all_order_by += col.column + " " + col.order_type + " , "
        all_order_by = all_order_by[:-3]

        # VALUES
        first_time = True
        values_list = []
        index = 0
        all_values = "VALUES\n"
        for value in self.values:
            if index == self.values_batch:
                all_values = all_values[:-1]
                values_list.append(all_values)
                index = 0
                all_values = "VALUES\n"
            if first_time and self.has_header:
                first_time = False
                continue
            all_values += "(" + str(value) + "),"
            index += 1
        all_values = all_values[:-1]
        if all_values!="VALUES":
            values_list.append(all_values)

        #######################################################################################
        if self.need_drop_table:
            query += "DROP TABLE " + self.target_table + ";\n\n"

        if self.need_create_table:
            query += "CREATE TABLE "+ self.target_table +" (\n"
            for col in self.columns_and_specs:
                query += col + ",\n"
            query = query[:-2]
            query+=");\n\n"

        if self.is_truncate:
            if self.database.upper() == CONNECTION_SQLITE.upper():
                query += "DELETE FROM " + self.target_table +";\n\n"
            else:
                query += "TRUNCATE TABLE " + self.target_table +";\n\n"

        if self.type == QUERY_TYPE_SELECT or self.type == QUERY_TYPE_INSERT or self.type == QUERY_TYPE_VIEW:

            if self.type == QUERY_TYPE_INSERT: query += "INSERT INTO " + self.target_table + "(" + all_insert_columns + ")\n"

            if self.type == QUERY_TYPE_VIEW:
                if self.database == CONNECTION_SQLITE: query += "DROP VIEW IF EXISTS " + self.target_table + ";\n"
                query += "CREATE VIEW " + self.target_table + " AS "

            if self.is_with: query += "WITH " + self.name_query + " AS (\n"

            # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
            firstTime = True
            for subquery in self.subqueries[::-1]:
                if not firstTime:
                    subquery = str(subquery)[5:]
                firstTime = False
                query += str(subquery) + ",\n"
            if len(self.subqueries)>0: query = query[:-2] + "\n"

            if self.is_distinct:
                query += "SELECT DISTINCT "
            else:
                query += "SELECT "
            query += all_select_columns + "\nFROM " + all_from_tables + "\n"
            if all_where_filters != "": query += "WHERE " + all_where_filters + "\n"
            if all_group_by_columns != "": query += "GROUP BY " + all_group_by_columns + "\n"
            if all_having_columns != "": query += "HAVING " + all_having_columns + "\n"
            if all_order_by != "": query += "ORDER BY " + all_order_by + "\n"

            if len(self.union_query)>0:
                for union_query in self.union_query:
                    query += "UNION\n" + str(union_query)

            if self.is_with: query += ")"

        if self.type == QUERY_TYPE_VALUES:
            for x in values_list:
                query += "INSERT INTO " + self.target_table + "(" + all_insert_columns + ")\n"
                query += x
                query += ";"
            if len(self.values) <= 1 and self.has_header: query = ""
            if len(values_list)==0: query = ""

            if (len(self.values) <= 1 and self.has_header) or len(values_list)==0:
                if self.need_drop_table:
                    if self.database.upper() == CONNECTION_SQLITE.upper():
                        query += "DELETE FROM " + self.target_table + ";\n\n"
                    else:
                        query += "TRUNCATE TABLE " + self.target_table + ";\n\n"

        if self.type == QUERY_TYPE_DELETE:
            where = ""
            if len(self.where_filters)>1:
                for where_filter in self.where_filters:
                    where += where_filter + " AND "
                where = where[:-4]
            else:
                where = self.where_filters[0]
            query += "DELETE FROM " + self.target_table + " WHERE " + where

        if self.type == QUERY_TYPE_UPDATE:
            raise ValueError("QUERY UPDATE not implemented yet")



        return query

    def validate_query_elements(self):
        """Permits to validate if all the parameters of the query can generate a result"""
        if len(self.subqueries) > 0 and self.is_with: raise ValueError("Impossible Query: a With Query can't have any With subquery")
        if self.is_with and self.name_query=="": raise ValueError("Impossible Query: a With Query needs to have a Name")
        if self.is_with and self.type!=QUERY_TYPE_SELECT: raise ValueError("Impossible Query: Only a SELECT query can be defined as WITH")
        if len(self.from_tables) == 0 and len(self.from_tables_and_relations) == 0 and self.type!=QUERY_TYPE_VALUES and self.type!=QUERY_TYPE_DELETE and self.is_truncate == False: raise ValueError("Impossible Query: there is no source table")
        if len(self.select_columns) == 0 and self.type!=QUERY_TYPE_VALUES and self.type!=QUERY_TYPE_DELETE and self.is_truncate == False: raise ValueError("Impossible Query: there is no columns to be selected")
        if len(self.where_filters) > 0 and len(self.having_filters) > 0: raise ValueError( "Impossible Query: is impossible to have a HAVING and WHERE clause.")

    def get_join_from_id(self, id: int):
        if id == JOIN_TYPE_INNER:
            result = "INNER JOIN"
        elif id == JOIN_TYPE_MASTER:
            result = "LEFT JOIN"
        elif id == JOIN_TYPE_DETAIL:
            result = "RIGHT JOIN"
        elif id == JOIN_TYPE_OUTER:
            result = "FULL OUTER JOIN"
        else:
            raise ValueError("Join doesn't exist")
        return result

class FromRelationQuery:
    def __init__(self, master_table: str, master_column: str, detail_table: str, detail_column: str, join_type: str, join_sign: str):
        self.master_table = master_table
        self.master_column = master_column
        self.detail_table = detail_table
        self.detail_column = detail_column
        self.join_type = join_type
        self.join_sign = join_sign

    def __str__(self):
        return self.master_table + "." + self.master_column + self.join_sign + self.detail_table + "." + self.detail_column + " - " + str(self.join_type)

class OrderByQuery:
    def __init__(self, column: str, order_type: str):
        self.column = column
        self.order_type = order_type
