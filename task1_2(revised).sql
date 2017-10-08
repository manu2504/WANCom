create temporary table table20 as (select idMeasurement,idPath,timestamp_ns div 1000000000 as time from Measurements where idPath in (select idPath from Paths where idTraceDirection=12));

select count(idPath) from Paths where idTraceDirection=20;


 ALTER TABLE `table20` ADD COLUMN `id` INT AUTO_INCREMENT UNIQUE FIRST;
use  test; 
create table Table20 ( id int auto_increment, idMeasurement int, idPath int, time bigint(20), PRIMARY KEY (id));
use wan;

INSERT INTO test.Table20 select * from wan.table12;
use test;


create table t20 as select e1.id, e1.idPath, e1.idPath src, e2.idPath dst, e1.time from_time, e2.time to_time, (e2.time -e1.time) as duration from Table12 e1 INNER JOIN Table12 e2 on e2.id =e1.id +1;



create table a as select idPath, sum(abs(duration)) as persistence ,count(id) as times from t20 where src=dst group by idPath;


create table b as select idPath, persistence div times as av_persistence from a;

create table c as select av_persistence, count(idPath) as sum from b group by av_persistence;

insert into c (sum,av_persistence) values (8,0);

create table cdf20 as select av_persistence as persistence, sum/22 as pdf from c order by av_persistence;


  ALTER TABLE `cdf20` ADD COLUMN `cdf` decimal(24,4);

set @csum :=0;

 update cdf20 set cdf = (@csum := @csum + pdf) order by persistence;


select * from cdf20;

SELECT * FROM  cdf20 INTO OUTFIlE '/var/lib/mysql-files/c_d_f20.csv';

drop table a,b, c;