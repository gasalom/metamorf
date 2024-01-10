/********************** RESET DATABASE ***********************/
DROP TABLE IF EXISTS OM_DATASET_HARDCODED;
DROP TABLE IF EXISTS OM_DATASET_PATH;
DROP TABLE IF EXISTS OM_PROPERTIES;
DROP TABLE IF EXISTS OM_REF_JOIN_TYPE;
DROP TABLE IF EXISTS OM_REF_KEY_TYPE;
DROP TABLE IF EXISTS OM_REF_MODULES;
DROP TABLE IF EXISTS OM_REF_ORDER_TYPE;
DROP TABLE IF EXISTS OM_REF_QUERY_TYPE;
DROP TABLE IF EXISTS OM_REF_ENTITY_TYPE;
DROP TABLE IF EXISTS ENTRY_ENTITY;
DROP TABLE IF EXISTS ENTRY_FILTERS;
DROP TABLE IF EXISTS ENTRY_ORDER;
DROP TABLE IF EXISTS ENTRY_HAVING;
DROP TABLE IF EXISTS ENTRY_PATH;
DROP TABLE IF EXISTS ENTRY_AGGREGATORS;
DROP TABLE IF EXISTS ENTRY_DATASET_MAPPINGS;
DROP TABLE IF EXISTS ENTRY_DATASET_RELATIONSHIPS;
DROP TABLE IF EXISTS OM_DATASET;
DROP TABLE IF EXISTS OM_DATASET_DV;
DROP TABLE IF EXISTS OM_DATASET_EXECUTION;
DROP TABLE IF EXISTS OM_DATASET_SPECIFICATION;
DROP TABLE IF EXISTS OM_DATASET_T_AGG;
DROP TABLE IF EXISTS OM_DATASET_T_DISTINCT;
DROP TABLE IF EXISTS OM_DATASET_T_FILTER;
DROP TABLE IF EXISTS OM_DATASET_T_HAVING;
DROP TABLE IF EXISTS OM_DATASET_T_MAPPING;
DROP TABLE IF EXISTS OM_DATASET_T_ORDER;
DROP TABLE IF EXISTS OM_DATASET_RELATIONSHIPS;
DROP TABLE IF EXISTS GIT_ENTRY_ENTITY;
DROP TABLE IF EXISTS GIT_ENTRY_FILTERS;
DROP TABLE IF EXISTS GIT_ENTRY_ORDER;
DROP TABLE IF EXISTS GIT_ENTRY_HAVING;
DROP TABLE IF EXISTS GIT_ENTRY_PATH;
DROP TABLE IF EXISTS GIT_ENTRY_AGGREGATORS;
DROP TABLE IF EXISTS GIT_ENTRY_DATASET_MAPPINGS;
DROP TABLE IF EXISTS GIT_ENTRY_DATASET_RELATIONSHIPS;
DROP VIEW IF EXISTS OM_DATASET_INFORMATION;
DROP VIEW IF EXISTS OM_RELATIONSHIPS;
DROP VIEW IF EXISTS OM_DATASET_SPECIFICATION_INFORMATION;
DROP TABLE IF EXISTS ENTRY_DV_MAPPINGS;
DROP TABLE IF EXISTS ENTRY_DV_ENTITY;
drop table if exists ENTRY_DV_PROPERTIES;
drop table if exists GIT_ENTRY_DV_ENTITY;
drop table if exists GIT_ENTRY_DV_MAPPINGS;
drop table if exists GIT_ENTRY_DV_PROPERTIES;
drop table if exists ENTRY_FILES;
drop table if exists GIT_ENTRY_FILES;
drop table if exists OM_DATASET_FILE;

/********************** CREATION TABLES **********************/
CREATE TABLE ENTRY_PATH (
	COD_PATH             varchar NOT NULL  ,
	DATABASE_NAME        varchar   ,
	SCHEMA_NAME          varchar   ,
	OWNER                varchar NOT NULL  ,
	CONSTRAINT "Pk_ENTRY_PATH_COD_PATH" PRIMARY KEY ( COD_PATH, OWNER )
 );

CREATE TABLE GIT_ENTRY_PATH (
	COD_PATH             varchar NOT NULL  ,
	DATABASE_NAME        varchar   ,
	SCHEMA_NAME          varchar   ,
	OWNER                varchar NOT NULL  ,
	CONSTRAINT "Pk_ENTRY_PATH_COD_PATH_0" PRIMARY KEY ( COD_PATH, OWNER )
 );

CREATE TABLE OM_DATASET_HARDCODED (
	ID_DATASET_HARDCODED number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	CONTENT              varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_HARDCODED_ID_DATASET_HARDCODED" PRIMARY KEY ( ID_DATASET_HARDCODED )
 );

ALTER TABLE OM_DATASET_HARDCODED SET COMMENT = 'Sustituo del mapping. ¿Debería incluirse en specifications entonces?';

CREATE TABLE OM_DATASET_PATH (
	ID_PATH              number NOT NULL  ,
	DATABASE_NAME        varchar   ,
	SCHEMA_NAME          varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Unq_OM_PATH_ID_PATH" UNIQUE ( ID_PATH ),
	CONSTRAINT "Pk_OM_PATH_ID_PATH" PRIMARY KEY ( ID_PATH )
 );

CREATE TABLE OM_PROPERTIES (
	PROPERTY             varchar   ,
	VALUE                varchar   ,
	START_DATE           timestamp
 );

CREATE TABLE OM_REF_JOIN_TYPE (
	ID_JOIN_TYPE         number NOT NULL  ,
	JOIN_NAME            varchar   ,
	JOIN_VALUE           varchar   ,
	JOIN_DESCRIPTION     varchar   ,
	CONSTRAINT "Pk_OEM_REF_JOIN_TYPE_ID_JOIN_TYPE" PRIMARY KEY ( ID_JOIN_TYPE ),
	CONSTRAINT "Unq_OEM_REF_JOIN_TYPE_JOIN_NAME" UNIQUE ( JOIN_NAME )
 );

CREATE TABLE OM_REF_KEY_TYPE (
	ID_KEY_TYPE          number NOT NULL  ,
	KEY_TYPE_NAME        varchar   ,
	KEY_TYPE_DESCRIPTION varchar   ,
	CONSTRAINT "Pk_OM_REF_KEY_TYPE_ID_KEY_TYPE" PRIMARY KEY ( ID_KEY_TYPE ),
	CONSTRAINT "Unq_OM_REF_KEY_TYPE_KEY_TYPE_NAME" UNIQUE ( KEY_TYPE_NAME )
 );

CREATE TABLE OM_REF_MODULES (
	ID_MODULE            number   ,
	MODULE_NAME          varchar   ,
	MODULE_FULL_NAME     varchar   ,
	MODULE_DESCRIPTION   varchar   ,
	CONSTRAINT "Unq_OM_REF_MODULES_ID_MODULE" UNIQUE ( ID_MODULE )
 );

CREATE TABLE OM_REF_ORDER_TYPE (
	ID_ORDER_TYPE        number NOT NULL  ,
	ORDER_TYPE_NAME      varchar   ,
	ORDER_TYPE_VALUE     varchar   ,
	ORDER_TYPE_DESCRIPTION varchar   ,
	CONSTRAINT "Pk_OM_REF_ORDER_TYPE_ID_ORDER_TYPE" PRIMARY KEY ( ID_ORDER_TYPE ),
	CONSTRAINT "Unq_OM_REF_ORDER_TYPE_ORDER_TYPE_NAME" UNIQUE ( ORDER_TYPE_NAME ),
	CONSTRAINT "Unq_OM_REF_ORDER_TYPE_ORDER_TYPE_VALUE" UNIQUE ( ORDER_TYPE_VALUE )
 );

CREATE TABLE OM_REF_QUERY_TYPE (
	ID_QUERY_TYPE        number NOT NULL  ,
	QUERY_TYPE_NAME      varchar   ,
	QUERY_TYPE_DESCRIPTION varchar   ,
	CONSTRAINT "Pk_OM_REF_QUERY_TYPE_ID_QUERY_TYPE" PRIMARY KEY ( ID_QUERY_TYPE ),
	CONSTRAINT "Unq_OM_REF_QUERY_TYPE_QUERY_TYPE_NAME" UNIQUE ( QUERY_TYPE_NAME )
 );

CREATE TABLE OM_REF_ENTITY_TYPE (
	ID_ENTITY_TYPE       number NOT NULL  ,
	ENTITY_TYPE_NAME     varchar   ,
	ENTITY_TYPE_DESCRIPTION varchar   ,
	ENTITY_TYPE_FULL_NAME varchar   ,
	ID_MODULE            number   ,
	CONSTRAINT "Pk_OM_REF_ENTITY_TYPE_ID_ENTITY_TYPE" PRIMARY KEY ( ID_ENTITY_TYPE ),
	CONSTRAINT "Idx_OM_REF_ENTITY_TYPE" UNIQUE ( ENTITY_TYPE_NAME )
 );

CREATE TABLE ENTRY_DV_ENTITY (
	COD_ENTITY           varchar NOT NULL  ,
	ENTITY_NAME          varchar   ,
	ENTITY_TYPE          varchar   ,
	COD_PATH             varchar   ,
	NAME_STATUS_TRACKING_SATELLITE varchar   ,
	NAME_RECORD_TRACKING_SATELLITE varchar   ,
	NAME_EFFECTIVITY_SATELLITE varchar   ,
	OWNER                varchar NOT NULL  ,
	CONSTRAINT "Pk_ENTRY_DV_ENTITY_COD_ENTITY" PRIMARY KEY ( COD_ENTITY, OWNER )
 );

CREATE TABLE ENTRY_DV_PROPERTIES (
	COD_ENTITY           varchar   ,
	NUM_CONNECTION       varchar   ,
	HASH_NAME            varchar   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_ENTITY (
	COD_ENTITY           varchar NOT NULL  ,
	TABLE_NAME           varchar   ,
	ENTITY_TYPE          varchar   ,
	COD_PATH             varchar   ,
	STRATEGY             varchar   ,
	OWNER                varchar NOT NULL  ,
	CONSTRAINT "Pk_ENTRY_DATASET_COD_ENTITY" PRIMARY KEY ( COD_ENTITY, OWNER )
 );

CREATE TABLE ENTRY_FILES (
	COD_ENTITY           varchar   ,
	FILE_PATH            varchar   ,
	FILE_NAME            varchar   ,
	DELIMITER_CHARACTER  varchar   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_FILTERS (
	COD_ENTITY_TARGET    varchar   ,
	VALUE                varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_HAVING (
	COD_ENTITY_TARGET    varchar   ,
	VALUE                varchar   ,
	NUM_BRANCH           varchar   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_ORDER (
	COD_ENTITY_TARGET    varchar   ,
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME          varchar   ,
	ORDER_TYPE           varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_DV_ENTITY (
	COD_ENTITY           varchar NOT NULL  ,
	ENTITY_NAME          varchar   ,
	ENTITY_TYPE          varchar   ,
	COD_PATH             varchar   ,
	NAME_STATUS_TRACKING_SATELLITE varchar   ,
	NAME_RECORD_TRACKING_SATELLITE varchar   ,
	NAME_EFFECTIVITY_SATELLITE varchar   ,
	OWNER                varchar   ,
	CONSTRAINT "Pk_ENTRY_DV_ENTITY_COD_ENTITY_0" PRIMARY KEY ( COD_ENTITY )
 );

CREATE TABLE GIT_ENTRY_DV_MAPPINGS (
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME_SOURCE   varchar   ,
	COD_ENTITY_TARGET    varchar   ,
	COLUMN_NAME_TARGET   varchar   ,
	COLUMN_TYPE_TARGET   varchar   ,
	ORDINAL_POSITION     number   ,
	COLUMN_LENGTH        number   ,
	COLUMN_PRECISION     number   ,
	NUM_BRANCH           number   ,
	NUM_CONNECTION       number   ,
	KEY_TYPE             varchar   ,
	SATELLITE_NAME       varchar   ,
	ORIGIN_IS_INCREMENTAL number   ,
	ORIGIN_IS_TOTAL      number   ,
	ORIGIN_IS_CDC        number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_DV_PROPERTIES (
	COD_ENTITY           varchar   ,
	NUM_CONNECTION       varchar   ,
	HASH_NAME            varchar   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_ENTITY (
	COD_ENTITY           varchar NOT NULL  ,
	TABLE_NAME           varchar   ,
	ENTITY_TYPE          varchar   ,
	COD_PATH             varchar   ,
	STRATEGY             varchar   ,
	OWNER                varchar NOT NULL  ,
	CONSTRAINT "Pk_ENTRY_DATASET_COD_ENTITY_0" PRIMARY KEY ( COD_ENTITY, OWNER )
 );

CREATE TABLE GIT_ENTRY_FILES (
	COD_ENTITY           varchar   ,
	FILE_PATH            varchar   ,
	FILE_NAME            varchar   ,
	DELIMITER_CHARACTER  varchar   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_FILTERS (
	COD_ENTITY_TARGET    varchar   ,
	VALUE                varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_HAVING (
	COD_ENTITY_TARGET    varchar   ,
	VALUE                varchar   ,
	NUM_BRANCH           varchar   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_ORDER (
	COD_ENTITY_TARGET    varchar   ,
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME          varchar   ,
	ORDER_TYPE           varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE OM_DATASET (
	ID_DATASET           number NOT NULL  AUTOINCREMENT,
	DATASET_NAME         varchar   ,
	ID_ENTITY_TYPE       number   ,
	ID_PATH              number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_Table_ID_DATASET" PRIMARY KEY ( ID_DATASET )
 );

CREATE TABLE OM_DATASET_DV (
	ID_DATASET           number   ,
	ID_ENTITY_TYPE       number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp
 );

CREATE TABLE OM_DATASET_EXECUTION (
	ID_DATASET           number   ,
	ID_QUERY_TYPE        number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp
 );

CREATE TABLE OM_DATASET_FILE (
	ID_DATASET           number   ,
	FILE_PATH            varchar   ,
	FILE_NAME            varchar   ,
	DELIMITER_CHARACTER  varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp
 );

CREATE TABLE OM_DATASET_SPECIFICATION (
	ID_DATASET_SPEC      number NOT NULL  ,
	ID_DATASET           number   ,
	ID_KEY_TYPE          number   ,
	COLUMN_NAME          varchar   ,
	COLUMN_TYPE          varchar   ,
	ORDINAL_POSITION     number   ,
	IS_NULLABLE          number   ,
	COLUMN_LENGTH        number   ,
	COLUMN_PRECISION     number   ,
	COLUMN_SCALE         number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_SPECIFICATION_ID_DATASET_SPEC" PRIMARY KEY ( ID_DATASET_SPEC )
 );

CREATE TABLE OM_DATASET_T_AGG (
	ID_T_AGG             number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	ID_DATASET_SPEC      number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_AGG_ID_T_AGG" PRIMARY KEY ( ID_T_AGG )
 );

CREATE TABLE OM_DATASET_T_DISTINCT (
	ID_T_DISTINCT        number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	SW_DISTINCT          number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_DISTINCT_ID_T_DISTINCT" PRIMARY KEY ( ID_T_DISTINCT )
 );

CREATE TABLE OM_DATASET_T_FILTER (
	ID_T_FILTER          number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	VALUE_FILTER         varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_FILTER_ID_T_FILTER" PRIMARY KEY ( ID_T_FILTER )
 );

CREATE TABLE OM_DATASET_T_HAVING (
	ID_T_HAVING          number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	VALUE_HAVING         varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_HAVING_ID_T_HAVING" PRIMARY KEY ( ID_T_HAVING )
 );

CREATE TABLE OM_DATASET_T_MAPPING (
	ID_T_MAPPING         number NOT NULL  ,
	ID_BRANCH            number   ,
	ID_DATASET_SPEC      number   ,
	VALUE_MAPPING        varchar   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_MAPPING_ID_MAPPING" PRIMARY KEY ( ID_T_MAPPING )
 );

CREATE TABLE OM_DATASET_T_ORDER (
	ID_T_ORDER           number NOT NULL  ,
	ID_DATASET           number   ,
	ID_BRANCH            number   ,
	ID_DATASET_SPEC      number   ,
	ID_ORDER_TYPE        number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_DATASET_T_ORDER_ID_T_ORDER" PRIMARY KEY ( ID_T_ORDER )
 );

CREATE TABLE ENTRY_AGGREGATORS (
	COD_ENTITY_TARGET    varchar   ,
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME          varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_DATASET_MAPPINGS (
	COD_ENTITY_SOURCE    varchar   ,
	VALUE_SOURCE         varchar   ,
	COD_ENTITY_TARGET    varchar   ,
	COLUMN_NAME_TARGET   varchar   ,
	COLUMN_TYPE_TARGET   varchar   ,
	ORDINAL_POSITION     number   ,
	COLUMN_LENGTH        number   ,
	COLUMN_PRECISION     number   ,
	NUM_BRANCH           number   ,
	KEY_TYPE             varchar   ,
	SW_DISTINCT          number   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_DATASET_RELATIONSHIPS (
	COD_ENTITY_MASTER    varchar   ,
	COLUMN_NAME_MASTER   varchar   ,
	COD_ENTITY_DETAIL    varchar   ,
	COLUMN_NAME_DETAIL   varchar   ,
	RELATIONSHIP_TYPE    varchar   ,
	OWNER                varchar
 );

CREATE TABLE ENTRY_DV_MAPPINGS (
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME_SOURCE   varchar   ,
	COD_ENTITY_TARGET    varchar   ,
	COLUMN_NAME_TARGET   varchar   ,
	COLUMN_TYPE_TARGET   varchar   ,
	ORDINAL_POSITION     number   ,
	COLUMN_LENGTH        number   ,
	COLUMN_PRECISION     number   ,
	NUM_BRANCH           number   ,
	NUM_CONNECTION       number   ,
	KEY_TYPE             varchar   ,
	SATELLITE_NAME       varchar   ,
	ORIGIN_IS_INCREMENTAL number   ,
	ORIGIN_IS_TOTAL      number   ,
	ORIGIN_IS_CDC        number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_AGGREGATORS (
	COD_ENTITY_TARGET    varchar   ,
	COD_ENTITY_SOURCE    varchar   ,
	COLUMN_NAME          varchar   ,
	NUM_BRANCH           number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_DATASET_MAPPINGS (
	COD_ENTITY_SOURCE    varchar   ,
	VALUE_SOURCE         varchar   ,
	COD_ENTITY_TARGET    varchar   ,
	COLUMN_NAME_TARGET   varchar   ,
	COLUMN_TYPE_TARGET   varchar   ,
	ORDINAL_POSITION     number   ,
	COLUMN_LENGTH        number   ,
	COLUMN_PRECISION     number   ,
	NUM_BRANCH           number   ,
	KEY_TYPE             varchar   ,
	SW_DISTINCT          number   ,
	OWNER                varchar
 );

CREATE TABLE GIT_ENTRY_DATASET_RELATIONSHIPS (
	COD_ENTITY_MASTER    varchar   ,
	COLUMN_NAME_MASTER   varchar   ,
	COD_ENTITY_DETAIL    varchar   ,
	COLUMN_NAME_DETAIL   varchar   ,
	RELATIONSHIP_TYPE    varchar   ,
	OWNER                varchar
 );

CREATE TABLE OM_DATASET_RELATIONSHIPS (
	ID_RELATIONSHIP      number NOT NULL  ,
	ID_DATASET_SPEC_MASTER number   ,
	ID_DATASET_SPEC_DETAIL number   ,
	ID_JOIN_TYPE         number   ,
	META_OWNER           varchar   ,
	START_DATE           timestamp   ,
	END_DATE             timestamp   ,
	CONSTRAINT "Pk_OM_RELATIONSHIPS_ID_RELATIONSHIP" PRIMARY KEY ( ID_RELATIONSHIP )
 );

CREATE VIEW OM_DATASET_INFORMATION AS select A.META_OWNER, B.ENTITY_TYPE_FULL_NAME, B.ENTITY_TYPE_DESCRIPTION, C.MODULE_NAME, C.MODULE_FULL_NAME, C.MODULE_DESCRIPTION, A.DATASET_NAME,  D.DATABASE_NAME, D.SCHEMA_NAME, F.QUERY_TYPE_NAME , F.QUERY_TYPE_DESCRIPTION , A.START_DATE
From OM_DATASET A
LEFT JOIN OM_REF_ENTITY_TYPE B on A.ID_ENTITY_TYPE = B.ID_ENTITY_TYPE
LEFT JOIN OM_REF_MODULES C on B.ID_MODULE = C.ID_MODULE
LEFT JOIN OM_DATASET_PATH D on A.ID_PATH = D.ID_PATH
LEFT JOIN OM_DATASET_EXECUTION E on A.ID_DATASET = E.ID_DATASET
LEFT JOIN OM_REF_QUERY_TYPE F on E.ID_QUERY_TYPE = F.ID_QUERY_TYPE
WHERE A.END_DATE is null and D.END_DATE is null and E.END_DATE is null;

CREATE VIEW OM_DATASET_SPECIFICATION_INFORMATION AS select A.META_OWNER , A.DATASET_NAME , B.COLUMN_NAME , B.COLUMN_TYPE , B.ORDINAL_POSITION , B.IS_NULLABLE , B.COLUMN_LENGTH , B.COLUMN_PRECISION , B.COLUMN_SCALE
FROM OM_DATASET A
LEFT JOIN OM_DATASET_SPECIFICATION B on A.ID_DATASET = B.ID_DATASET
WHERE A.END_DATE is null and B.END_DATE is null;

CREATE VIEW OM_RELATIONSHIPS AS select A.META_OWNER , D.DATABASE_NAME as MASTER_DATABASE_NAME, D.SCHEMA_NAME as MASTER_SCHEMA_NAME, C.DATASET_NAME as MASTER_DATASET_NAME, B.COLUMN_NAME as MASTER_COLUMN_NAME,
 G.DATABASE_NAME as DETAIL_DATABASE_NAME , G.SCHEMA_NAME as DETAIL_SCHEMA_NAME, F.DATASET_NAME  as DETAIL_DATASET_NAME, E.COLUMN_NAME as DETAIL_COLUMN_NAME, A.START_DATE
from OM_DATASET_RELATIONSHIPS A
LEFT JOIN OM_DATASET_SPECIFICATION B on A.ID_DATASET_SPEC_MASTER = B.ID_DATASET_SPEC
LEFT JOIN OM_DATASET C on B.ID_DATASET = C.ID_DATASET
LEFT JOIN OM_DATASET_PATH D on C.ID_PATH = D.ID_PATH
LEFT JOIN OM_DATASET_SPECIFICATION E on A.ID_DATASET_SPEC_DETAIL  = E.ID_DATASET_SPEC
LEFT JOIN OM_DATASET F on E.ID_DATASET = F.ID_DATASET
LEFT JOIN OM_DATASET_PATH G on G.ID_PATH = F.ID_PATH
where A.END_DATE is null and B.END_DATE is null and C.END_DATE is null and D.END_DATE is null and E.END_DATE is null and F.END_DATE is null and G.END_DATE is null;



-- INSERTS
INSERT INTO OM_REF_MODULES(ID_MODULE, MODULE_NAME, MODULE_FULL_NAME, MODULE_DESCRIPTION) VALUES
(0, 'ELT', 'Transformation', 'Offers transformation for data'),
(1, 'DV', 'Data Vault', 'Generates the processes for the different datavault entities');

INSERT INTO OM_REF_ENTITY_TYPE (ID_ENTITY_TYPE, ENTITY_TYPE_NAME, ENTITY_TYPE_DESCRIPTION, ENTITY_TYPE_FULL_NAME, ID_MODULE) VALUES
(0, 'SRC', 'Source of the run. It need to be loaded from other sources', 'Source', 0),
(1, 'VIEW', 'Temporary table. It will be not materialized', 'Temporary', 0),
(2, 'TB', 'Table. It''s the result of a process', 'Table', 0),
(3, 'WITH', 'With Clause', 'With', 0),
(4, 'HUB', 'Datavault - Hub', 'Hub', 1),
(5, 'LINK', 'Datavault - Link', 'Link', 1),
(6, 'SAT', ' Datavault - Satellite', 'Satellite', 1),
(7, 'STS', 'Datavault - Status Tracking Satellite', 'Status Tracking Satellite', 1),
(8, 'RTS', 'Datavault - Satellite', 'Record Tracking Satellite', 1),
(9, 'SATE', 'Datavault - Effectivity Satellite', 'Effectivity Satellite', 1);

INSERT INTO OM_REF_JOIN_TYPE(ID_JOIN_TYPE, JOIN_NAME, JOIN_VALUE, JOIN_DESCRIPTION) VALUES
(0, 'INNER JOIN', 'INNER JOIN', 'Returns only those rows that have matching values'),
(1, 'MASTER JOIN', 'LEFT JOIN', 'Returns those rows from the left table plus those that have matching values'),
(2, 'DETAIL JOIN', 'RIGHT JOIN', 'Returns those rows from the right table plus those that have matching values'),
(3, 'OUTER JOIN', 'OUTER JOIN', 'Returns rows from both tables');

INSERT INTO OM_REF_KEY_TYPE(ID_KEY_TYPE, KEY_TYPE_NAME, KEY_TYPE_DESCRIPTION) VALUES
(0, 'PK', 'Primary Key'), (1, 'BK', 'Business Key'), (2,'NULL', 'Nothing'), (3,'SEQ', 'Sequence'),
(4, 'FK', 'Foreign Key'), (5, 'HK', 'Hash Key'), (6, 'AT', 'Attribute'), (7 ,'ST','Status'),
(8, 'DK', 'Driven Key'), (9, 'RS', 'Record Source'), (10, 'TN', 'Tenant'), (11,'HD', 'Hashdiff'),
(12, 'DCK', 'Dependent-child key'), (13, 'AD', 'Applied Date');

INSERT INTO OM_REF_ORDER_TYPE(ID_ORDER_TYPE, ORDER_TYPE_NAME, ORDER_TYPE_VALUE, ORDER_TYPE_DESCRIPTION) VALUES
(0, 'Ascendant', 'ASC', 'Ascending order'),
(1, 'Descendant', 'DESC', 'Descending order');

INSERT INTO OM_REF_QUERY_TYPE(ID_QUERY_TYPE, QUERY_TYPE_NAME, QUERY_TYPE_DESCRIPTION) VALUES
(0, 'INSERT', 'Insert on the target table'),
(1, 'UPDATE', 'Update based on the Primary Key'),
(2, 'VIEW', 'Creates a View'),
(3, 'DELETE', 'Deletes based on the Primary Key'),
(4, 'SELECT', 'Select the target query'),
(5, 'MERGE', 'Select the target query'),
(6, 'TRUNCATE AND INSERT', 'Truncate the target table and inserts'),
(7, 'DROP AND INSERT', 'Drop the target table and inserts');

INSERT INTO OM_PROPERTIES(PROPERTY, "VALUE", START_DATE) VALUES
('Version', '0.4.5.1', CURRENT_TIMESTAMP()),
('Module Deployed', 'ELT', CURRENT_TIMESTAMP()),
('Module Deployed', 'DV', CURRENT_TIMESTAMP());