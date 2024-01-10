from __future__ import annotations
from metamorf.constants import *

class Query:

    def __init__(self):
        # Query Type: Insert, Update, View, Delete, Merge, Select, Truncate & Insert or Values
        self.type = None
        # Name Query: Name of the WITH clause. It's mandatory for the WITH query types
        self.name_query = ""
        # Target Table: Name of the target table of the query
        self.target_table = ""
        # Is With: Flag to indicate if the query object is a with query type.
        self.is_with = False
        # Is Distinct: Flag to indicate if the query has distinct clause
        self.is_distinct = False
        # Insert Columns: Array with all the columns that will be on the insert clause
        self.insert_columns = []
        # Select Columns: Array with all the columns (value as column_name) that will be on the main select clause
        self.select_columns = []
        # From Table: Tables that will be on the 'From' clause. If there are more than one, it will generate cartesian product
        self.from_tables = []
        # From Tables and Relations: All the relations that will be on the FROM clause. All this array is made it from FromRelationQuery Objects defined on this file
        self.from_tables_and_relations = []
        # Group By Columns: Array with all the columns that will be on the GROUP BY clause
        self.group_by_columns = []
        # Having Filters: Array with all the columns that will be on the HAVING clause.
        self.having_filters = []
        # Order by Columns: Array with all the columns that will be on the ORDER BY clause. ALl the objects need to be OrderByQuery objects defined on this file.
        self.order_by_columns = []
        # Where Filters: Array with all the filters that will be on the WHERE clause.
        self.where_filters = []
        # Primary Key: Array with all the columns that are defined as Primary Key
        self.primary_key = []
        # Subqueries: QUERY objects (this object type) that will be included on the WITH clause
        self.subqueries = []
        # Union Query: QUERY object that will be included on the UNION clause. It needs to be setted as SELECT query type. If the main query has with clause, it need to be included on the main query.
        self.union_query = []
        # Values: Array with all the rows that will be included on the VALUES clause. Each row doesn't need parenthesis
        self.values = []
        # Has Header: Flag to indicate if the VALUES includes header. If it's TRUE, the first row from VALUES is skipped
        self.has_header = False
        # Values Batch: Number of rows on VALUES clause for each INSERT. By default is 1000.
        self.values_batch = 1000 # Num of values that an insert can execute
        # Columns and Specifications: Array with "COLUMN_NAME COLUMN_TYPE" to indicate all the specification for the target query
        self.columns_and_specs = []
        # Database: Database Type need to be setted [Sqlite, MySql, Snowflake, Firebird, PostreSql)
        self.database = None
        # Is Truncate: Flag to indicate if the target table needs to be truncated
        self.is_truncate = False
        # Need Create Table: Flag to indicate if the target table needs to be created
        self.need_create_table = False
        # Need Drop Table: Flag to indicate if the target table needs to be dropped
        self.need_drop_table = False
        # Columns In Database: If it is indicated, the table already exists on the database and has the columns indicated on this variable. Array with "COLUMN_NAME COLUMN_TYPE]
        self.columns_in_database = []

    def set_database(self, database: str):
        '''Set the Target database of the query. Use the constants CONNECTION_[X]'''
        self.database = database

    def set_columns_in_database(self, columns_in_database: list):
        self.columns_in_database = columns_in_database

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

    def add_from_tables(self, from_tables: list):
        if isinstance(from_tables, str):
            from_tables = [from_tables]
        for x in from_tables:
            self.from_tables.append(x)

    def set_from_tables_and_relations(self, from_tables_and_relations: list):
        for from_table in from_tables_and_relations:
            if not isinstance(from_table, FromRelationQuery): raise TypeError("FromRelationQuery must be set to an FromRelationQuery Object")
        self.from_tables_and_relations = from_tables_and_relations

    def add_from_tables_and_relations(self, from_tables_and_relations: list):
        for from_table in from_tables_and_relations:
            if not isinstance(from_table, FromRelationQuery): raise TypeError("FromRelationQuery must be set to an FromRelationQuery Object")
        for x in from_tables_and_relations:
            self.from_tables_and_relations.append(x)

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

        for union_query in query.union_query:
            for x in union_query.from_tables:
                if x not in all_from_tables: all_from_tables.append(x)
            for x in union_query.from_tables_and_relations:
                if x.master_table not in all_from_tables: all_from_tables.append(x.master_table)
                if x.detail_table not in all_from_tables: all_from_tables.append(x.detail_table)

        return all_from_tables

    def get_database_target(self):
        return self.name_query.split('.')[0]

    def get_schema_target(self):
        if self.database == CONNECTION_SQLITE: return None
        return self.name_query.split('.')[1]

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
        all_relation_to_include = self.from_tables_and_relations.copy()
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
        if self.need_drop_table: query += "DROP TABLE " + self.target_table + ";\n\n"

        if self.need_create_table:
            query += "CREATE TABLE "+ self.target_table +" (\n"
            for col in self.columns_and_specs:
                query += col + ",\n"

            if len(self.primary_key)>0:
                query += "PRIMARY KEY ("
                for pk in self.primary_key:
                    query += pk.split('.')[1] + ','
                query = query[:-1]
                query += ")"
            else:
                query = query[:-2]
            query+=");\n\n"

        if len(self.columns_in_database)>0 and self.need_drop_table is False and self.need_create_table is False:
            for col_metadata in self.columns_and_specs:
                is_found = False
                for col_database in self.columns_in_database:
                    if col_metadata.split(' ')[0] == col_database[0]:
                        is_found = True
                        break
                if is_found:
                    continue
                else:
                    query += "ALTER TABLE " + self.name_query + " ADD COLUMN " + col_metadata + ";\n"

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

            # In case there is no data to load, and DROP TABLE is setted to TRUE => all the data is deleted
            if (len(self.values) <= 1 and self.has_header) or len(values_list)==0:
                if self.need_drop_table:
                    if self.database.upper() == CONNECTION_SQLITE.upper():
                        query += "DELETE FROM " + self.target_table + ";\n\n"
                    else:
                        query += "TRUNCATE TABLE " + self.target_table + ";\n\n"

        if self.type == QUERY_TYPE_DELETE and len(self.primary_key)==0 and len(self.select_columns) == 0:
            where = ""
            if len(self.where_filters)>1:
                for where_filter in self.where_filters:
                    where += where_filter + " AND "
                where = where[:-4]
            else:
                where = self.where_filters[0]
            query += "DELETE FROM " + self.target_table + " WHERE " + where

        if self.type == QUERY_TYPE_DELETE and len(self.primary_key)>0 and len(self.select_columns)>0:

            if self.database.upper() == CONNECTION_SQLITE.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "DELETE FROM "+ self.target_table +"\n"
                query += "WHERE EXISTS \n"
                query += "(select * from " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP WHERE \n"
                for pk in self.primary_key:
                    query += self.target_table +"."+pk.split('.')[1] + "=" +self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk.split('.')[1] +" AND\n"
                query = query[:-4]
                query += ")"

            if self.database.upper() == CONNECTION_MYSQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "DELETE FROM "+ self.target_table +"\n"
                query += "USING "+ self.target_table +"\n"
                query += "JOIN " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP ON \n"
                for pk in self.primary_key:
                    query += self.target_table +"."+pk.split('.')[1] + "=" +self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk.split('.')[1] +" AND\n"
                query = query[:-4]

            if self.database.upper() == CONNECTION_SNOWFLAKE.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries+
                with_clause_string = ""
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    with_clause_string += str(subquery) + ",\n"
                if len(self.subqueries) > 0: with_clause_string = with_clause_string[:-2] + "\n"

                query += "DELETE FROM "+ self.target_table +"\n"
                query += "WHERE USING ( \n" + with_clause_string + " select * From " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP ) as " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP \n"
                query += " WHERE \n"
                for pk in self.primary_key:
                    query += self.target_table +"."+pk.split('.')[1] + "=" +self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk.split('.')[1] +" AND\n"
                query = query[:-4]

            if self.database.upper() == CONNECTION_POSTGRESQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "DELETE FROM "+ self.target_table +" " + self.get_dataset_name_from_fqdn(self.target_table) + "\n"
                query += "WHERE  \n"
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) + "." + pk.split('.')[1] +','
                query = query[:-1]
                query += ' in \n'
                query += "(select "
                for pk in self.primary_key:
                    query += pk.split('.')[1] +','
                    query = query[:-1]
                query +=" from " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP )"

        if self.type == QUERY_TYPE_UPDATE:

            if self.database.upper() == CONNECTION_SQLITE.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "UPDATE "+ self.target_table + " AS " + self.get_dataset_name_from_fqdn(self.target_table) +"\n"
                query += "SET (\n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += col + ",\n"
                query = query[:-2] +"\n)\n = (\n"
                query += "SELECT "
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += self.get_dataset_name_from_fqdn(self.target_table) +"__TMP."+ col+ ",\n"
                query = query[:-2] +"\n"
                query += "FROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP WHERE "
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) +"."+pk.split('.')[1] + "=" +self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk.split('.')[1] +" AND\n"
                query = query[:-4] +")\n"
                query += "WHERE ("
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) +"."+pk.split('.')[1] +","
                query = query[:-1] + ")"
                query += " IN (select "
                for pk in self.primary_key:
                    query += pk.split('.')[1] +","
                query = query[:-1]
                query += " FROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP )"

            if self.database.upper() == CONNECTION_MYSQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "UPDATE "+ self.target_table + " " + self.get_dataset_name_from_fqdn(self.target_table) +"\n"

                query += "INNER JOIN " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP ON "
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) + "." + pk.split('.')[1] + "=" + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP." + pk.split('.')[1] + " AND\n"
                query = query[:-4] + "\n"

                query += "SET \n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += self.get_dataset_name_from_fqdn(self.target_table) +"." + col + "=" + self.get_dataset_name_from_fqdn(self.target_table) +"__TMP." + col +",\n"
                query = query[:-2] +"\n"

            if self.database.upper() == CONNECTION_POSTGRESQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0,new_query) # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "UPDATE "+ self.target_table + " AS " + self.get_dataset_name_from_fqdn(self.target_table) +"\n"
                query += "SET (\n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += col + ",\n"
                query = query[:-2] +"\n)\n = (\n"
                query += "SELECT "
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += self.get_dataset_name_from_fqdn(self.target_table) +"__TMP."+ col+ ",\n"
                query = query[:-2] +"\n"
                query += "FROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP WHERE "
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) +"."+pk.split('.')[1] + "=" +self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk.split('.')[1] +" AND\n"
                query = query[:-4] +")\n"
                query += "WHERE ("
                for pk in self.primary_key:
                    query += self.get_dataset_name_from_fqdn(self.target_table) +"."+pk.split('.')[1] +","
                query = query[:-1] + ")"
                query += " IN (select "
                for pk in self.primary_key:
                    query += pk.split('.')[1] +","
                query = query[:-1]
                query += " FROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP )"

            if self.database.upper() == CONNECTION_SNOWFLAKE.upper():
                raise ValueError("UPDATE Snowflake not developped")

        if self.type == QUERY_TYPE_MERGE:

            if self.database.upper() == CONNECTION_SQLITE.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0, new_query)  # Add the main select to the last WITH clause

                query += "INSERT INTO " + self.target_table + "(" + all_insert_columns + ")\n"
                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "SELECT " + ','.join([str(col) for col in self.insert_columns]) + " FROM "+ self.get_dataset_name_from_fqdn(self.target_table) + "__TMP" + " WHERE TRUE "
                query += "ON CONFLICT ("
                for pk in self.primary_key:
                    query += pk + ","
                query = query[:-1]
                query += ") DO UPDATE SET "
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += col + "=excluded." + col + ", "
                query = query[:-2]

            if self.database.upper() == CONNECTION_SNOWFLAKE.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0, new_query)  # Add the main select to the last WITH clause

                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"

                query += "MERGE INTO " + self.target_table + " TARGET_TABLE\nUSING ("

                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"
                query += " select * From " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP\n) TMP_TABLE\nON"

                for pk in self.primary_key:
                    query += "TARGET_TABLE." + pk + " = TMP_TABLE." + pk +" AND\n"
                query = query[:-5]
                query += "\nWHEN MATCHED THEN UPDATE SET\n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += "TARGET_TABLE." + col + " = TMP_TABLE."+ col + " and\n "
                query = query[:-5]
                query += "\nWHEN NOT MATCHED THEN INSERT("+all_insert_columns+") VALUES (" + all_insert_columns + ")"

            if self.database.upper() == CONNECTION_MYSQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0, new_query)  # Add the main select to the last WITH clause

                query += "INSERT INTO " + self.target_table +"(" + all_insert_columns +")\n"

                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"
                if len(self.subqueries) > 0: query = query[:-2] + "\n"
                query += "SELECT "+all_insert_columns+"\nFROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP\n"
                query += "ON DUPLICATE KEY UPDATE\n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += self.target_table + "." + col + " = " + self.get_dataset_name_from_fqdn(self.target_table) +"__TMP."+ col + ",\n"
                query = query[:-2]

            if self.database.upper() == CONNECTION_POSTGRESQL.upper():
                new_query = Query()
                new_query.set_name_query(self.get_dataset_name_from_fqdn(self.target_table) + "__TMP")
                new_query.set_target_table(self.target_table)
                new_query.set_columns_and_specs(self.columns_and_specs)
                new_query.set_is_with(True)
                new_query.set_type(QUERY_TYPE_SELECT)
                new_query.set_select_columns(self.select_columns)
                new_query.set_from_tables(self.from_tables)
                new_query.set_is_distinct(self.is_distinct)
                new_query.set_from_tables_and_relations(self.from_tables_and_relations)
                new_query.set_insert_columns(self.insert_columns)
                new_query.set_order_by_columns(self.order_by_columns)
                new_query.set_having_filters(self.having_filters)
                new_query.set_group_by_columns(self.group_by_columns)
                new_query.set_primary_key(self.primary_key)
                new_query.set_where_filters(self.where_filters)
                self.subqueries.insert(0, new_query)  # Add the main select to the last WITH clause

                # Add all WITH subqueries: it deletes with clause if there are more than 2 subqueries
                firstTime = True
                for subquery in self.subqueries[::-1]:
                    if not firstTime:
                        subquery = str(subquery)[5:]
                    firstTime = False
                    query += str(subquery) + ",\n"

                query += "updated AS (\n"
                query += "UPDATE " +  self.target_table  + " AS "+ self.get_dataset_name_from_fqdn(self.target_table) + " SET \n"
                for col in self.insert_columns:
                    if col not in [x.split('.')[1] for x in self.primary_key]:
                        query += col + "=" + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP." + col + ",\n"
                query = query[:-2]
                query += "\nFROM " + self.get_dataset_name_from_fqdn(self.target_table) + "__TMP\nWHERE\n"
                for pk in [x.split('.')[1] for x in self.primary_key]:
                    query += self.get_dataset_name_from_fqdn(self.target_table) +"."+pk + "="+self.get_dataset_name_from_fqdn(self.target_table) + "__TMP."+pk +" AND\n"
                query = query[:-5]
                query += "\nRETURNING " + self.get_dataset_name_from_fqdn(self.target_table) + ".*\n)\n"
                query +="INSERT INTO " + self.target_table + "\nSELECT * FROM " +  self.get_dataset_name_from_fqdn(self.target_table) + "__TMP\n"
                query += "WHERE ("
                all_primary_key = ""
                for pk in [x.split('.')[1] for x in self.primary_key]:
                    all_primary_key += pk+","
                all_primary_key = all_primary_key[:-1]
                query += all_primary_key + ") NOT IN (SELECT " + all_primary_key + " FROM updated)"



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
