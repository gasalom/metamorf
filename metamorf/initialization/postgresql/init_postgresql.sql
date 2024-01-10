/********************** RESET DATABASE ***********************/
DROP TABLE if exists OM_DATASET_HARDCODED CASCADE;
DROP TABLE if exists OM_DATASET_PATH CASCADE;
DROP TABLE if exists OM_PROPERTIES CASCADE;
DROP TABLE if exists ENTRY_FILTERS CASCADE;
DROP TABLE if exists ENTRY_ORDER CASCADE;
DROP TABLE if exists ENTRY_HAVING CASCADE;
DROP TABLE if exists ENTRY_PATH CASCADE;
DROP TABLE if exists ENTRY_AGGREGATORS CASCADE;
DROP TABLE if exists ENTRY_DATASET_MAPPINGS CASCADE;
DROP TABLE if exists ENTRY_DATASET_RELATIONSHIPS CASCADE;
DROP TABLE if exists OM_DATASET CASCADE;
DROP TABLE IF EXISTS OM_DATASET_DV CASCADE;
DROP TABLE if exists OM_DATASET_EXECUTION CASCADE;
DROP TABLE if exists OM_DATASET_SPECIFICATION CASCADE;
DROP TABLE if exists OM_DATASET_T_AGG CASCADE;
DROP TABLE if exists OM_DATASET_T_DISTINCT CASCADE;
DROP TABLE if exists OM_DATASET_T_FILTER CASCADE;
DROP TABLE if exists OM_DATASET_T_HAVING CASCADE;
DROP TABLE if exists OM_DATASET_T_MAPPING CASCADE;
DROP TABLE if exists OM_DATASET_T_ORDER CASCADE;
DROP TABLE if exists OM_DATASET_RELATIONSHIPS CASCADE;
DROP TABLE if exists GIT_ENTRY_ENTITY CASCADE;
DROP TABLE if exists GIT_ENTRY_FILTERS CASCADE;
DROP TABLE if exists GIT_ENTRY_ORDER CASCADE;
DROP TABLE if exists GIT_ENTRY_HAVING CASCADE;
DROP TABLE if exists GIT_ENTRY_PATH CASCADE;
DROP TABLE if exists GIT_ENTRY_AGGREGATORS CASCADE;
DROP TABLE if exists GIT_ENTRY_DATASET_MAPPINGS CASCADE;
DROP TABLE if exists GIT_ENTRY_DATASET_RELATIONSHIPS CASCADE;
DROP VIEW if exists OM_DATASET_INFORMATION CASCADE;
DROP VIEW if exists OM_RELATIONSHIPS CASCADE;
DROP VIEW if exists OM_DATASET_SPECIFICATION_INFORMATION CASCADE;
DROP TABLE if exists ENTRY_DV_MAPPINGS CASCADE;
DROP TABLE if exists ENTRY_DV_ENTITY CASCADE;
drop table if exists ENTRY_DV_PROPERTIES CASCADE;
drop table if exists GIT_ENTRY_DV_ENTITY CASCADE;
drop table if exists GIT_ENTRY_DV_MAPPINGS CASCADE;
drop table if exists GIT_ENTRY_DV_PROPERTIES CASCADE;
DROP TABLE if exists OM_REF_JOIN_TYPE CASCADE;
DROP TABLE if exists OM_REF_KEY_TYPE CASCADE;
DROP TABLE if exists OM_REF_MODULES CASCADE;
DROP TABLE if exists OM_REF_ORDER_TYPE CASCADE;
DROP TABLE if exists OM_REF_QUERY_TYPE CASCADE;
DROP TABLE if exists OM_REF_ENTITY_TYPE CASCADE;
DROP TABLE if exists ENTRY_ENTITY CASCADE;
drop table if exists ENTRY_FILES CASCADE;
drop table if exists GIT_ENTRY_FILES CASCADE;
drop table if exists OM_DATASET_FILE CASCADE;

/********************** CREATION TABLES **********************/
CREATE TABLE ENTRY_PATH ( 
	COD_PATH           text  NOT NULL    ,
	DATABASE_NAME      text      ,
	SCHEMA_NAME        text      ,
	OWNER              text  NOT NULL    ,
	PRIMARY KEY ( COD_PATH, OWNER )
 );

CREATE TABLE GIT_ENTRY_PATH ( 
	COD_PATH           text  NOT NULL    ,
	DATABASE_NAME      text      ,
	SCHEMA_NAME        text      ,
	OWNER              text  NOT NULL    ,
	PRIMARY KEY ( COD_PATH, OWNER )
 );

CREATE TABLE OM_DATASET_HARDCODED ( 
	ID_DATASET_HARDCODED integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	CONTENT            text      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_PATH ( 
	ID_PATH            integer  NOT NULL,
	DATABASE_NAME      text      ,
	SCHEMA_NAME        text      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp      ,
	UNIQUE ( ID_PATH )
 );

CREATE TABLE OM_PROPERTIES ( 
	PROPERTY           text      ,
	VALUE              text      ,
	START_DATE         timestamp
 );

CREATE TABLE OM_REF_JOIN_TYPE ( 
	ID_JOIN_TYPE       integer  NOT NULL,
	JOIN_NAME          text      ,
	JOIN_VALUE         text      ,
	JOIN_DESCRIPTION   text      ,
	UNIQUE ( JOIN_NAME )
 );

CREATE TABLE OM_REF_KEY_TYPE ( 
	ID_KEY_TYPE        integer  NOT NULL,
	KEY_TYPE_NAME      text      ,
	KEY_TYPE_DESCRIPTION text      ,
	UNIQUE ( KEY_TYPE_NAME )
 );

CREATE TABLE OM_REF_MODULES ( 
	ID_MODULE          integer      ,
	MODULE_NAME        text      ,
	MODULE_FULL_NAME   text      ,
	MODULE_DESCRIPTION text      ,
	UNIQUE ( ID_MODULE )
 );

CREATE TABLE OM_REF_ORDER_TYPE ( 
	ID_ORDER_TYPE      integer  NOT NULL,
	ORDER_TYPE_NAME    text      ,
	ORDER_TYPE_VALUE   text      ,
	ORDER_TYPE_DESCRIPTION text      ,
	UNIQUE ( ORDER_TYPE_NAME ) ,
	UNIQUE ( ORDER_TYPE_VALUE )
 );

CREATE TABLE OM_REF_QUERY_TYPE ( 
	ID_QUERY_TYPE      integer  NOT NULL,
	QUERY_TYPE_NAME    text      ,
	QUERY_TYPE_DESCRIPTION text      ,
	UNIQUE ( QUERY_TYPE_NAME )
 );

CREATE TABLE OM_REF_ENTITY_TYPE ( 
	ID_ENTITY_TYPE     integer  NOT NULL,
	ENTITY_TYPE_NAME   text      ,
	ENTITY_TYPE_DESCRIPTION text      ,
	ENTITY_TYPE_FULL_NAME text      ,
	ID_MODULE          integer      ,
	UNIQUE ( ENTITY_TYPE_NAME )
 );

CREATE TABLE ENTRY_DV_ENTITY ( 
	COD_ENTITY         text  NOT NULL,
	ENTITY_NAME        text      ,
	ENTITY_TYPE        text      ,
	COD_PATH           text      ,
	NAME_STATUS_TRACKING_SATELLITE text      ,
	NAME_RECORD_TRACKING_SATELLITE text      ,
	NAME_EFFECTIVITY_SATELLITE text      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_DV_PROPERTIES ( 
	COD_ENTITY         text      ,
	NUM_CONNECTION     text      ,
	HASH_NAME          text      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_ENTITY ( 
	COD_ENTITY         text  NOT NULL    ,
	TABLE_NAME         text      ,
	ENTITY_TYPE        text      ,
	COD_PATH           text      ,
	STRATEGY           text      ,
	OWNER              text  NOT NULL    ,
	PRIMARY KEY ( COD_ENTITY, OWNER )
 );

CREATE TABLE ENTRY_FILTERS ( 
	COD_ENTITY_TARGET  text      ,
	VALUE              text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_HAVING ( 
	COD_ENTITY_TARGET  text      ,
	VALUE              text      ,
	NUM_BRANCH         text      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_ORDER ( 
	COD_ENTITY_TARGET  text      ,
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME        text      ,
	ORDER_TYPE         text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_DV_ENTITY ( 
	COD_ENTITY         text  NOT NULL,
	ENTITY_NAME        text      ,
	ENTITY_TYPE        text      ,
	COD_PATH           text      ,
	NAME_STATUS_TRACKING_SATELLITE text      ,
	NAME_RECORD_TRACKING_SATELLITE text      ,
	NAME_EFFECTIVITY_SATELLITE text      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_DV_MAPPINGS ( 
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME_SOURCE text      ,
	COD_ENTITY_TARGET  text      ,
	COLUMN_NAME_TARGET text      ,
	COLUMN_TYPE_TARGET text      ,
	ORDINAL_POSITION   integer      ,
	COLUMN_LENGTH      integer      ,
	COLUMN_PRECISION   integer      ,
	NUM_BRANCH         integer      ,
	NUM_CONNECTION     integer      ,
	KEY_TYPE           text      ,
	SATELLITE_NAME     text      ,
	ORIGIN_IS_INCREMENTAL integer      ,
	ORIGIN_IS_TOTAL    integer      ,
	ORIGIN_IS_CDC      integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_DV_PROPERTIES ( 
	COD_ENTITY         text      ,
	NUM_CONNECTION     text      ,
	HASH_NAME          text      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_ENTITY ( 
	COD_ENTITY         text  NOT NULL    ,
	TABLE_NAME         text      ,
	ENTITY_TYPE        text      ,
	COD_PATH           text      ,
	STRATEGY           text      ,
	OWNER              text  NOT NULL    ,
	PRIMARY KEY ( COD_ENTITY, OWNER )
 );

CREATE TABLE GIT_ENTRY_FILTERS ( 
	COD_ENTITY_TARGET  text      ,
	VALUE              text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_HAVING ( 
	COD_ENTITY_TARGET  text      ,
	VALUE              text      ,
	NUM_BRANCH         text      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_ORDER ( 
	COD_ENTITY_TARGET  text      ,
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME        text      ,
	ORDER_TYPE         text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE OM_DATASET ( 
	ID_DATASET         integer  NOT NULL,
	DATASET_NAME       text      ,
	ID_ENTITY_TYPE     integer      ,
	ID_PATH            integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_EXECUTION ( 
	ID_DATASET         integer      ,
	ID_QUERY_TYPE      integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_SPECIFICATION ( 
	ID_DATASET_SPEC    integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_KEY_TYPE        integer      ,
	COLUMN_NAME        text      ,
	COLUMN_TYPE        text      ,
	ORDINAL_POSITION   integer      ,
	IS_NULLABLE        integer      ,
	COLUMN_LENGTH      integer      ,
	COLUMN_PRECISION   integer      ,
	COLUMN_SCALE       integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_AGG ( 
	ID_T_AGG           integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	ID_DATASET_SPEC    integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_DISTINCT ( 
	ID_T_DISTINCT      integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	SW_DISTINCT        integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_FILTER ( 
	ID_T_FILTER        integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	VALUE_FILTER       text      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_HAVING ( 
	ID_T_HAVING        integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	VALUE_HAVING       text      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_MAPPING ( 
	ID_T_MAPPING       integer  NOT NULL,
	ID_BRANCH          integer      ,
	ID_DATASET_SPEC    integer      ,
	VALUE_MAPPING      text      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE OM_DATASET_T_ORDER ( 
	ID_T_ORDER         integer  NOT NULL,
	ID_DATASET         integer      ,
	ID_BRANCH          integer      ,
	ID_DATASET_SPEC    integer      ,
	ID_ORDER_TYPE      integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

CREATE TABLE ENTRY_AGGREGATORS ( 
	COD_ENTITY_TARGET  text      ,
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME        text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_DATASET_MAPPINGS ( 
	COD_ENTITY_SOURCE  text      ,
	VALUE_SOURCE       text      ,
	COD_ENTITY_TARGET  text      ,
	COLUMN_NAME_TARGET text      ,
	COLUMN_TYPE_TARGET text      ,
	ORDINAL_POSITION   integer      ,
	COLUMN_LENGTH      integer      ,
	COLUMN_PRECISION   integer      ,
	NUM_BRANCH         integer      ,
	KEY_TYPE           text      ,
	SW_DISTINCT        integer      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_DATASET_RELATIONSHIPS ( 
	COD_ENTITY_MASTER  text      ,
	COLUMN_NAME_MASTER text      ,
	COD_ENTITY_DETAIL  text      ,
	COLUMN_NAME_DETAIL text      ,
	RELATIONSHIP_TYPE  text      ,
	OWNER              text      
 );

CREATE TABLE ENTRY_DV_MAPPINGS ( 
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME_SOURCE text      ,
	COD_ENTITY_TARGET  text      ,
	COLUMN_NAME_TARGET text      ,
	COLUMN_TYPE_TARGET text      ,
	ORDINAL_POSITION   integer      ,
	COLUMN_LENGTH      integer      ,
	COLUMN_PRECISION   integer      ,
	NUM_BRANCH         integer      ,
	NUM_CONNECTION     integer      ,
	KEY_TYPE           text      ,
	SATELLITE_NAME     text      ,
	ORIGIN_IS_INCREMENTAL integer      ,
	ORIGIN_IS_TOTAL    integer      ,
	ORIGIN_IS_CDC      integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_AGGREGATORS ( 
	COD_ENTITY_TARGET  text      ,
	COD_ENTITY_SOURCE  text      ,
	COLUMN_NAME        text      ,
	NUM_BRANCH         integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_DATASET_MAPPINGS ( 
	COD_ENTITY_SOURCE  text      ,
	VALUE_SOURCE       text      ,
	COD_ENTITY_TARGET  text      ,
	COLUMN_NAME_TARGET text      ,
	COLUMN_TYPE_TARGET text      ,
	ORDINAL_POSITION   integer      ,
	COLUMN_LENGTH      integer      ,
	COLUMN_PRECISION   integer      ,
	NUM_BRANCH         integer      ,
	KEY_TYPE           text      ,
	SW_DISTINCT        integer      ,
	OWNER              text      
 );

CREATE TABLE GIT_ENTRY_DATASET_RELATIONSHIPS ( 
	COD_ENTITY_MASTER  text      ,
	COLUMN_NAME_MASTER text      ,
	COD_ENTITY_DETAIL  text      ,
	COLUMN_NAME_DETAIL text      ,
	RELATIONSHIP_TYPE  text      ,
	OWNER              text      
 );

CREATE TABLE OM_DATASET_RELATIONSHIPS ( 
	ID_RELATIONSHIP    integer  NOT NULL,
	ID_DATASET_SPEC_MASTER integer      ,
	ID_DATASET_SPEC_DETAIL integer      ,
	ID_JOIN_TYPE       integer      ,
	META_OWNER         text      ,
	START_DATE         timestamp      ,
	END_DATE           timestamp
 );

  CREATE TABLE OM_DATASET_DV (
	ID_DATASET           integer     ,
	ID_ENTITY_TYPE       integer     ,
	META_OWNER           text     ,
	START_DATE           timestamp     ,
	END_DATE             timestamp
 );

CREATE TABLE ENTRY_FILES (
	COD_ENTITY           text     ,
	FILE_PATH            text     ,
	FILE_NAME            text     ,
	DELIMITER_CHARACTER  text     ,
	OWNER                text
 );

CREATE TABLE GIT_ENTRY_FILES (
	COD_ENTITY           text     ,
	FILE_PATH            text     ,
	FILE_NAME            text     ,
	DELIMITER_CHARACTER  text     ,
	OWNER                text
 );

CREATE TABLE OM_DATASET_FILE (
	ID_DATASET           integer     ,
	FILE_PATH            text     ,
	FILE_NAME            text     ,
	DELIMITER_CHARACTER  text     ,
	META_OWNER           text     ,
	START_DATE           timestamp     ,
	END_DATE             timestamp
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
(8, 'RTS', 'Datavault - Satellite', 'Record Tracking Satellite', '1'),
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

INSERT INTO OM_PROPERTIES(PROPERTY, VALUE, START_DATE) VALUES
('Version', '0.4.5.1',current_timestamp ),
('Module Deployed', 'ELT', current_timestamp),
('Module Deployed', 'DV', CURRENT_TIMESTAMP);