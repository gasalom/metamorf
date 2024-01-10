/********************** CREATE DATABASE ***********************/
create database if not exists METAMORF;
create or replace SCHEMA DATA;

/********************** RESET DATABASE ***********************/
drop table if exists PSA_CUSTOMERS;
drop table if exists PSA_SALES;

drop table if exists RTS_CUSTOMER;
drop table if exists HUB_CUSTOMER;
drop table if exists SAT_CUSTOMER_CONTACT;
drop table if exists SAT_CUSTOMER_INFO;
drop table if exists STS_CUSTOMER;
drop table if exists HUB_SHOP;
drop table if exists SAT_PRODUCT_INFO;
drop table if exists SAT_PRODUCT_PRICE_HISTORY;
drop table if exists HUB_PRODUCT;
drop table if exists HUB_INVOICE;
drop table if exists LINK_PURCHASE_DETAIL;
drop table if exists RTS_INVOICE;
drop table if exists STS_PRODUCT;
drop table if exists SAT_PURCHASE_INFO;

/******************** CREATION DATABASE **********************/
CREATE TABLE PSA_CUSTOMERS (
	CUSTOMER_ID INTEGER,
	CUSTOMER_EMAIL VARCHAR,
	CUSTOMER_PHONE VARCHAR,
	REGISTRATION_DATE VARCHAR
);

INSERT INTO PSA_CUSTOMERS (CUSTOMER_ID,CUSTOMER_EMAIL,CUSTOMER_PHONE,REGISTRATION_DATE) VALUES
(101,'juan@example.com','+34 111111111','07/01/2024'),
(101,'juan@example.com','+34 222222222','07/01/2024'),
(102,'ana@example.com','+34 333333333','01/01/2024'),
(103,'carlos@example.com','+34 444444444','10/01/2024'),
(104,'maria@example.com','+34 555555555','10/01/2024'),
(105,'andres@example.com','+34 666666666','05/01/2024'),
(105,'andres@example.com','+34 777777777','05/01/2024'),
(105,'andres@example.com','+34 888888888','05/01/2024');

CREATE TABLE PSA_SALES (
	CUSTOMER_ID INTEGER,
	SHOP_ID INTEGER,
	INVOICE_NO INTEGER,
	INVOICE_DATE VARCHAR,
	PRODUCT_NAME VARCHAR,
	PRODUCT_COLOR VARCHAR,
	PRODUCT_SIZE VARCHAR,
	QUANTITY INTEGER,
	UNIT_PRICE INTEGER,
	CUSTOMER_NAME VARCHAR
);

INSERT INTO PSA_SALES (CUSTOMER_ID,SHOP_ID,INVOICE_NO,INVOICE_DATE,PRODUCT_NAME,PRODUCT_COLOR,PRODUCT_SIZE,QUANTITY,UNIT_PRICE,CUSTOMER_NAME) VALUES
 (101,1,654654,'07/01/2024','Product A','Red','L',2,25.5,'Juan Perez'),
 (101,1,654654,'07/01/2024','Product B','Blue','M',3,12.75,'Juan Perez'),
 (102,2,8795,'08/01/2024','Product C','Green','S',2,18.0,'Emma Gomez'),
 (102,2,8795,'08/01/2024','Product A','Yellow','XL',2,25.5,'Emma Gomez'),
 (102,2,95641,'09/01/2024','Product B','Red','S',1,12.75,'Emma Gomez'),
 (103,1,95648,'09/01/2024','Product C','Blue','M',2,18.0,'Carlos Garcia'),
 (103,1,10002,'10/01/2024','Product A','Black','L',3,25.5,'Carlos Garcia'),
 (104,3,10002,'10/01/2024','Product B','White','XL',1,12.75,'Marta Lopez'),
 (105,2,65884,'11/01/2024','Product C','Green','M',3,18.0,'Andres Martinez'),
 (105,2,65884,'11/01/2024','Product A','Blue','S',2,25.5,'Andres Martinez'),
 (105,2,65884,'11/01/2024','Product B','Red','L',3,12.75,'Andres Martinez'),
 (106,1,393939,'12/01/2024','Product C','Green','XL',2,18.0,'Laura Garcia');





