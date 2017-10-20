/* To calculate the latency between datacentencers,
first create a temporary table which contains idPath,  rtt_ns, idTraceDirection */
create temporary table fyra 
select t1.idPath, t1.rtt_ns, t2.idTraceDirection from Measurements t1
left join Paths t2 on t2.idPath = t1.idPath 
union
select t2.idPath, t1.rtt_ns, t2.idTraceDirection from Measurements t1
left join Paths t2 on t2.idPath = t1.idPath;

/* Then calculate the average latency of all the paths in one trace
command below use trace 1, which is Ireland to Tokyo, as an example*/
select idTraceDirection, avg(rtt_ns)/1000000 as lat_ms
from fyra group by idTraceDirection;
