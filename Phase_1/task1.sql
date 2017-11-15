


#First I filter  all the idpaths belong to each pair of datacentres, for instance,for #idNodes 1 and 3(Ireland and Oregon), all idPaths are in idTraceDirection=2/9.And #I divide timestamp_ns to 1000000000 for better calculation further.
CREATE TEMPORARY TABLE 
IF NOT EXISTS table1 AS
 (SELECT idPath,FROM_UNIXTIME(MIN(timestamp_ns) div 1000000000) as startime FROM Measurements
 WHERE idPath  IN (SELECT idPath from Paths where idTraceDirection in (1,5)) 
GROUP BY idpath HAVING COUNT(*)>0);
# select the min(startime) of the new table above,to find the very beginning of new #paths appear.

select min (startime) from table1;

#For each hour increase, the startime(timestamp_ns div 1000000000) increase #3600.In that case I make a loop to measure how many paths appear per hour.

 delimiter $$
 drop procedure if exists wk;
create procedure wk()
 begin
  declare var int;
  set var = 0;
  while var <  60 do
  select count(idPath) from i where startime between 1499537000 + 3600*var and 1499537000 + 3600*(var+1);
 set var = var +1;
 end while;
 end $$
 delimiter ;
call wk();
