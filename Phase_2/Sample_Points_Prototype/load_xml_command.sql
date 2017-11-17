mysql> describe geoLocation;
+------------+------------------+------+-----+---------+-------+
| Field      | Type             | Null | Key | Default | Extra |
+------------+------------------+------+-----+---------+-------+
| locId      | int(10) unsigned | NO   | PRI | NULL    |       |
| country    | char(2)          | NO   |     | NULL    |       |
| region     | char(2)          | NO   |     | NULL    |       |
| city       | varchar(64)      | NO   |     | NULL    |       |
| postalCode | varchar(5)       | NO   |     | NULL    |       |
| latitude   | float            | YES  |     | NULL    |       |
| longitude  | float            | YES  |     | NULL    |       |
+------------+------------------+------+-----+---------+-------+


mysql> describe GeoIp;
+------------+------------------+------+-----+---------+-------+
| Field      | Type             | Null | Key | Default | Extra |
+------------+------------------+------+-----+---------+-------+
| startIpNum | int(10) unsigned | NO   | PRI | NULL    |       |
| endIpNum   | int(10) unsigned | NO   | PRI | NULL    |       |
| locId      | int(10) unsigned | NO   |     | NULL    |       |
+------------+------------------+------+-----+---------+-------+

mysql> describe Hops;
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| idHop         | int(11)     | NO   | PRI | NULL    | auto_increment |
| idPath        | int(11)     | NO   | MUL | NULL    |                |
| ipSrc         | varchar(15) | NO   |     | NULL    |                |
| ipDst         | varchar(15) | NO   |     | NULL    |                |
| idPredecessor | int(11)     | YES  | MUL | NULL    |                |
+---------------+-------------+------+-----+---------+----------------


 idHop | ipSrc          | locId  | country | region | city    | postalCode | latitude | longitude | startIpNum | endIpNum   |

 CREATE TABLE `LatLng_test1` (
  `idHop` int(11) NOT NULL PRIMARY KEY Auto_increment,
  `lat` float  NULL ,
  `lng` float  NULL 
);


LOAD XML LOCAL INFILE '/Users/vv/Desktop/elevation_API_test/test.xml' 
INTO TABLE LatLng_test1 rows identified by '<location>';

