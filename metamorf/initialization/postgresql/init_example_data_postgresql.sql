/********************** RESET DATABASE ***********************/
drop table if exists AIRCRAFTS;
drop table if exists AIRPORTS;
drop table if exists CARRIERS;
drop table if exists FLIGHTS;
drop table if exists CUSTOMERS;
drop table if exists USERS_WEB;
drop table if exists FLIGHTS_TMP;
drop table if exists AIRCRAFTS_TMP;
drop table if exists CUSTOMERS_TMP;
drop table if exists HUB_CUSTOMER;
drop table if exists HUB_FLIGHTS;
drop table if exists SAT_CUSTOMER_INFO;
drop table if exists SAT_FLIGHTS_ICAO;
drop table if exists SAT_CUSTOMER_LEGAL;
drop table if exists LINK_SELLS;
drop table if exists SAT_FLIGHTS_ICAO;
drop table if exists SAT_SELL_EVENT;
drop table if exists SAT_SELL_PROPERTIES;
drop table if exists SAT_LAST_APPEAR_DATE;
drop table if exists HUB_AIRPORTS;
drop table if exists LINK_AIRPORTS_FLIGHTS;
drop table if exists RTS_AIRPORTS;
drop table if exists RTS_CUSTOMER;
drop table if exists RTS_SELLS;
drop table if exists SATE_AIRPORTS_FLIGHTS;

/******************** CREATION DATABASE **********************/
CREATE TABLE AIRCRAFTS (
	LICENSE TEXT,
	MODEL_ICAO TEXT,
	NAME TEXT,
	AIRCRAFTS_BY TEXT,
	AIRCRAFTS_TYPE TEXT,
	APC TEXT,
	WTC TEXT,
	ALTERNATIVE_NAME TEXT,
	CARRIER_IATA TEXT
);

INSERT INTO AIRCRAFTS (LICENSE,MODEL_ICAO,NAME,AIRCRAFTS_BY,AIRCRAFTS_TYPE,APC,WTC,ALTERNATIVE_NAME,CARRIER_IATA) VALUES
 ('EC-GAS','A320','A320','AIRBUS','L2J','C','M','AIRBUS A-320','VY'),
 ('EC-ZOO','A320','A320','AIRBUS','L2J','C','M','AIRBUS A-320','VY'),
 ('I-RES','B738','737-800','BOEING','L2J','D','M','BOEING 737-800','FR'),
 ('G-YAK','A35K','A350-1000 XWB','AIRBUS','L2J','D','H','A-350-1000 XWB Prestige','BA'),
 ('I-HHH','A320','A320','AIRBUS','L2J','C','M','AIRBUS A-320','FR');

CREATE TABLE AIRPORTS (
	IDENT TEXT,
	AIRPORTS_TYPE TEXT,
	NAME TEXT,
	ELEVATION INTEGER,
	CONTINENT TEXT,
	ISO_COUNTRY TEXT,
	ISO_REGION TEXT,
	MUNICIPALITY TEXT,
	GPS_CODE TEXT,
	IATA_CODE TEXT,
	LOCAL_CODE TEXT,
	COORDINATES TEXT
);

INSERT INTO AIRPORTS (IDENT,AIRPORTS_TYPE,NAME,ELEVATION,CONTINENT,ISO_COUNTRY,ISO_REGION,MUNICIPALITY,GPS_CODE,IATA_CODE,LOCAL_CODE,COORDINATES) VALUES
 ('LEBL','large_airport','Barcelona International Airport',12,'EU','ES','ES-CT','Barcelona','LEBL','BCN','','41.2971, 2.07846'),
 ('LEPA','large_airport','Palma De Mallorca Airport',27,'EU','ES','ES-PM','Palma De Mallorca','LEPA','PMI','','39.551700592, 2.73881006241'),
 ('LIPE','large_airport','Bologna Guglielmo Marconi Airport',123,'EU','IT','IT-45','Bologna','LIPE','BLQ','BO08','44.5354, 11.2887'),
 ('LEIB','medium_airport','Ibiza Airport',24,'EU','ES','ES-PM','Ibiza','LEIB','IBZ','','38.872898101800004, 1.3731199502899998'),
 ('LEVC','medium_airport','Valencia Airport',240,'EU','ES','ES-V','Valencia','LEVC','VLC','','39.4893, -0.481625');

CREATE TABLE CARRIERS (
	ICAO TEXT,
	IATA TEXT,
	CALLSIGN TEXT,
	NAME TEXT,
	FOUNDED TEXT,
	COMMENCED_OPERATIONS TEXT,
	PARENT_COMPANY TEXT,
	FLEET_SIZE INTEGER,
	DESTINATIONS INTEGER
);

INSERT INTO CARRIERS (ICAO,IATA,CALLSIGN,NAME,FOUNDED,COMMENCED_OPERATIONS,PARENT_COMPANY,FLEET_SIZE,DESTINATIONS) VALUES
 ('VLG','VY','VUELING','Vueling Airlines','10/02/2004','01/07/2004','IAG',126,148),
 ('RYR','FR','RYAN','Ryanair','28/11/1984','08/07/1985','Ryanair Holdings plc',514,225),
 ('BAW','BA','SPEEDBIRD','Brithish Aiwrways','31/03/1974','31/03/1974','International Airlines Group',257,183);

CREATE TABLE FLIGHTS (
	UNIQUE_FLIGHT_CODE TEXT,
	FLIGHT_CODE TEXT,
	AIRPORT_ORIGIN_CODE TEXT,
	AIRPORT_DEST_CODE TEXT,
	DEPARTURE_GATE TEXT,
	BOARDING_TIME TEXT,
	DEPARTURE_TIME TEXT,
	LANDING_TIME TEXT,
	ARRIVAL_TIME TEXT,
	AIRCRAFT TEXT,
	BOARDING_TIME_REAL TEXT,
	DEPARTURE_TIME_REAL TEXT,
	LANDING_TIME_REAL TEXT,
	ARRIVAL_TIME_REAL TEXT,
	OPERATION TEXT
);

INSERT INTO FLIGHTS (UNIQUE_FLIGHT_CODE,FLIGHT_CODE,AIRPORT_ORIGIN_CODE,AIRPORT_DEST_CODE,DEPARTURE_GATE,BOARDING_TIME,DEPARTURE_TIME,LANDING_TIME,ARRIVAL_TIME,AIRCRAFT,BOARDING_TIME_REAL,DEPARTURE_TIME_REAL,LANDING_TIME_REAL,ARRIVAL_TIME_REAL,OPERATION) VALUES
 ('VLG390820221008','VLG3908','BCN','PMI','B39','08/10/2022 11:45','08/10/2022 11:55','08/10/2022 12:31','08/10/2022 12:40','EC-GAS','','','','','I'),
 ('VLG390920221008','VLG3909','PMI','BCN','D86','08/10/2022 13:15','08/10/2022 13:25','08/10/2022 14:01','08/10/2022 14:10','EC-ZOO','','','','','I'),
 ('RYR936620221008','RYR9366','BCN','BLQ','Terminal 2','08/10/2022 15:30','08/10/2022 15:40','08/10/2022 17:03','08/10/2022 17:13','I-RES','','','','','I'),
 ('BAW19020221007','BAW190','AUS','LHR','Terminal 5','07/10/2022 18:20','07/10/2022 18:30','07/10/2022 15:27','07/10/2022 15:45','G-YAK','','','','','I'),
 ('VLG369420221006','VLG3694','IBZ','VLC','Puerta 6','06/10/2022 13:25','06/10/2022 13:35','06/10/2022 14:06','06/10/2022 14:15','I-HHH','','','','','I');


CREATE TABLE CUSTOMERS (
    ID_CUSTOMER INTEGER,
    NAME TEXT,
    NIE TEXT,
    PRICE INTEGER,
    SELL_DATE TEXT,
    ADDRESS TEXT,
    NATIONALITY TEXT,
    FLIGHT_CODE TEXT
);

INSERT INTO CUSTOMERS (ID_CUSTOMER, NAME, NIE, PRICE, SELL_DATE, ADDRESS, NATIONALITY, FLIGHT_CODE) VALUES
(0, 'Guillermo Aumatell', 'ZAB000000', 30, '28/09/2022 16:03', 'Avda. Principal, 3o 4a', 'ES', 'VLG3694'),
(1, 'William Smith', '123456789', 28.50, '03/05/2022 12:24', 'Main Street, 48', 'UK', 'VLG3908');

CREATE TABLE USERS_WEB (
    ID_CUSTOMER INTEGER,
    VISIT_DATE TEXT,
    TIME_ONLINE_SECONDS INTEGER
);

insert into USERS_WEB (ID_CUSTOMER, VISIT_DATE, TIME_ONLINE_SECONDS) VALUES
(0, '26/09/2022 06:03', 124),(0, '27/09/2022 11:48', 82),(0, '28/09/2022 16:00', 501),
(1, '03/05/2022 12:23', 258), (1, '03/05/2022 12:22', 0);