create temporary table table12 as (select idMeasurement,idPath,timestamp_ns div 1000000000 as time from Measurements where idPath in (select idPath from Paths where idTraceDirection=12));

select count(idPath) from Paths where idTraceDirection=12;


 ALTER TABLE `table12` ADD COLUMN `id` INT AUTO_INCREMENT UNIQUE FIRST;
use  test; 
create table Table12 ( id int auto_increment, idMeasurement int, idPath int, time bigint(20), PRIMARY KEY (id));
use wan;

INSERT INTO test.Table12 select * from wan.table12;
use test;


  create table t12 as select e1.id, e1.idPath, e1.idPath src, e2.idPath dst, e1.time from_time, e2.time to_time, (e2.time -e1.time) as duration from Table12 e1 INNER JOIN Table12 e2 on e2.id =e1.id +1;



create table three as select idPath, (sum(duration)) as time_frame from ta1 where src = dst group by idPath;

create table three as select idPath, (sum(duration) div 3600 ) as time_frame from t3 where src = dst group by idPath;



select COUNT(idPath), time_frame from trace3result group by time_frame;

select COUNT(idPath) from trace3result;

