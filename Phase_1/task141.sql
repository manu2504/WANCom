/*To calculate the distribution of the number of network hops of each trace
first create a temporary table which contains the  idPath, idHop, idTraceDirection */
create temporary table kat 
select t1.idPath, t1.idHops, t2.idTraceDirection from Hops t1
left join Paths t2 on t2.idPath = t1.idPath
union
select t2.idPath, t1.idHop, t2.idTraceDirection from Hops t1
right join Paths t2 on t2.idPath = t1.idPath;

/*Then create temporary tables
 to see how many hops are there in all paths in one trace
 comand below use trace 1, which is from Ireland to Tokyo, as an exemple */
 create temporary table cou1
 select idPath, count(*) as numero from kat 
 where idTraceDirection = '1' group by idPath;
 
 /*Then counting how many paths in one trace that have certain numbers of hops */
 select numero, count(*) from cou1 group by numero;
 