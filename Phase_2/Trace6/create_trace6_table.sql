

CREATE TEMPORARY TABLE 
IF NOT EXISTS ip_trace6_with_3cables AS SELECT idHop,idPath,ipSrc,ipDst
FROM Hops WHERE ipSrc!= '*' AND ipDst!= '*'
AND idPath in (select idPath from Paths where idTraceDirection=6); 

ALTER TABLE ip_trace6_with_3cables ADD COLUMN id INT AUTO_INCREMENT NOT NULL, ADD primary key(id);

mysql> select * from table6;
+-------+--------+---------------+---------------+
| idHop | idPath | ipSrc         | ipDst         |
+-------+--------+---------------+---------------+
|   642 |     33 | 100.64.16.173 | 52.95.30.217  |
|   646 |     33 | 52.95.30.217  | 52.95.31.131  |
|   649 |     33 | 52.95.31.131  | 52.95.31.18   |
|   651 |     33 | 52.95.31.18   | 27.0.0.248    |
|   653 |     33 | 27.0.0.248    | 54.239.41.161 |
|   656 |     33 | 54.239.41.161 | 54.239.43.132 |
|   659 |     33 | 54.239.43.132 | 52.93.13.10   |
|   662 |     33 | 52.93.13.10   | 52.93.12.255  |
|   665 |     33 | 52.93.12.255  | 52.93.12.146  |
|   668 |     33 | 52.93.12.146  | 52.93.12.169  |
|   670 |     33 | 52.93.12.169  | 52.93.13.83   |
|  1201 |     56 | 100.64.16.173 | 52.95.30.217  |
|  1202 |     56 | 52.95.30.217  | 52.95.31.131  |
|  1208 |     56 | 27.0.0.248    | 54.239.41.161 |
|  1216 |     56 | 54.239.41.161 | 54.239.43.132 |
|  1225 |     56 | 54.239.43.132 | 52.93.13.10   |
|  1233 |     56 | 52.93.13.10   | 52.93.12.255  |
|  1239 |     56 | 52.93.12.255  | 52.93.12.146  |
|  1241 |     56 | 52.93.12.146  | 52.93.12.169  |
|  1243 |     56 | 52.93.12.169  | 52.93.13.83   |
|  2288 |    105 | 100.64.16.173 | 52.95.30.217  |
|  2291 |    105 | 52.95.30.217  | 52.95.31.131  |
|  2295 |    105 | 52.95.31.131  | 52.95.31.18   |
|  2300 |    105 | 52.95.31.18   | 27.0.0.248    |
|  2305 |    105 | 27.0.0.248    | 54.239.41.161 |
|  2310 |    105 | 54.239.41.161 | 54.239.43.132 |
|  2332 |    105 | 52.93.12.169  | 52.93.13.83   |
|  2475 |    114 | 100.64.16.173 | 52.95.30.217  |
|  2477 |    114 | 52.95.30.217  | 52.95.31.131  |
|  2479 |    114 | 52.95.31.131  | 52.95.31.18   |
|  2481 |    114 | 52.95.31.18   | 27.0.0.248    |
|  2483 |    114 | 27.0.0.248    | 54.239.41.161 |
|  2487 |    114 | 54.239.41.161 | 54.239.43.132 |
|  2495 |    114 | 52.93.12.255  | 52.93.12.146  |
|  2499 |    114 | 52.93.12.146  | 52.93.12.169  |
|  2502 |    114 | 52.93.12.169  | 52.93.13.83   |
|  2536 |    117 | 100.64.16.173 | 52.95.30.217  |
|  2538 |    117 | 52.95.30.217  | 52.95.31.131  |
|  2540 |    117 | 52.95.31.131  | 52.95.31.18   |
|  2542 |    117 | 52.95.31.18   | 27.0.0.248    |
|  2544 |    117 | 27.0.0.248    | 54.239.41.161 |
|  2546 |    117 | 54.239.41.161 | 54.239.43.132 |
|  2547 |    117 | 54.239.43.132 | 52.93.13.10   |
|  2549 |    117 | 52.93.13.10   | 52.93.12.255  |
|  2555 |    117 | 52.93.12.169  | 52.93.13.83   |
| 23749 |    994 | 100.64.16.173 | 52.95.30.217  |
| 23750 |    994 | 52.95.30.217  | 52.95.31.131  |
| 23752 |    994 | 52.95.31.131  | 52.95.31.18   |
| 23754 |    994 | 52.95.31.18   | 27.0.0.248    |
| 23755 |    994 | 27.0.0.248    | 54.239.41.161 |
| 23756 |    994 | 54.239.41.161 | 54.239.43.132 |
| 23765 |    994 | 52.93.12.169  | 52.93.13.83   |
| 23792 |    996 | 100.64.16.173 | 52.95.30.217  |
| 23794 |    996 | 52.95.30.217  | 52.95.31.131  |
| 23796 |    996 | 52.95.31.131  | 52.95.31.18   |
| 23800 |    996 | 52.95.31.18   | 27.0.0.248    |
| 23803 |    996 | 27.0.0.248    | 54.239.41.161 |
| 23805 |    996 | 54.239.41.161 | 54.239.43.132 |
| 23814 |    996 | 52.93.12.146  | 52.93.12.169  |
| 23816 |    996 | 52.93.12.169  | 52.93.13.83   |
| 24297 |   1017 | 100.64.16.173 | 52.95.30.217  |
| 24299 |   1017 | 52.95.30.217  | 52.95.31.131  |
| 24301 |   1017 | 52.95.31.131  | 52.95.31.18   |
| 24308 |   1017 | 54.239.41.161 | 54.239.43.132 |
| 24310 |   1017 | 54.239.43.132 | 52.93.13.10   |
| 24313 |   1017 | 52.93.13.10   | 52.93.12.255  |
| 24315 |   1017 | 52.93.12.255  | 52.93.12.146  |
| 24317 |   1017 | 52.93.12.146  | 52.93.12.169  |
| 24319 |   1017 | 52.93.12.169  | 52.93.13.83   |
| 25473 |   1063 | 52.95.30.217  | 52.95.31.131  |
| 25474 |   1063 | 52.95.31.131  | 52.95.31.18   |
| 25475 |   1063 | 52.95.31.18   | 27.0.0.248    |
| 25476 |   1063 | 27.0.0.248    | 54.239.41.161 |
| 25477 |   1063 | 54.239.41.161 | 54.239.43.132 |
| 25478 |   1063 | 54.239.43.132 | 52.93.13.10   |
| 25479 |   1063 | 52.93.13.10   | 52.93.12.255  |
| 25480 |   1063 | 52.93.12.255  | 52.93.12.146  |
| 25481 |   1063 | 52.93.12.146  | 52.93.12.169  |
| 25482 |   1063 | 52.93.12.169  | 52.93.13.83   |
| 30718 |   1272 | 100.64.16.173 | 52.95.30.217  |
| 30719 |   1272 | 52.95.30.217  | 52.95.31.131  |
| 30720 |   1272 | 52.95.31.131  | 52.95.31.18   |
| 30721 |   1272 | 52.95.31.18   | 27.0.0.248    |
| 30722 |   1272 | 27.0.0.248    | 54.239.41.161 |
| 30723 |   1272 | 54.239.41.161 | 54.239.43.132 |
| 30724 |   1272 | 54.239.43.132 | 52.93.13.10   |
| 30725 |   1272 | 52.93.13.10   | 52.93.12.255  |
| 30726 |   1272 | 52.93.12.255  | 52.93.12.146  |
| 31122 |   1289 | 100.64.16.173 | 52.95.30.217  |
| 31123 |   1289 | 52.95.30.217  | 52.95.31.131  |
| 31124 |   1289 | 52.95.31.131  | 52.95.31.18   |
| 31125 |   1289 | 52.95.31.18   | 27.0.0.248    |
| 31128 |   1289 | 54.239.43.132 | 52.93.13.10   |
| 31129 |   1289 | 52.93.13.10   | 52.93.12.255  |
| 31130 |   1289 | 52.93.12.255  | 52.93.12.146  |
| 31131 |   1289 | 52.93.12.146  | 52.93.12.169  |
| 31132 |   1289 | 52.93.12.169  | 52.93.13.83   |
| 38722 |   1604 | 100.64.16.173 | 52.95.30.217  |
| 38723 |   1604 | 52.95.30.217  | 52.95.31.131  |
| 38724 |   1604 | 52.95.31.131  | 52.95.31.18   |
| 38725 |   1604 | 52.95.31.18   | 27.0.0.248    |
| 38726 |   1604 | 27.0.0.248    | 54.239.41.161 |
| 38738 |   1604 | 52.93.12.169  | 52.93.13.83   |
| 38777 |   1608 | 100.64.16.173 | 52.95.30.217  |
| 38781 |   1608 | 52.95.30.217  | 52.95.31.131  |
| 38784 |   1608 | 52.95.31.131  | 52.95.31.18   |
| 38787 |   1608 | 52.95.31.18   | 27.0.0.248    |
| 38789 |   1608 | 27.0.0.248    | 54.239.41.161 |
| 38799 |   1608 | 52.93.13.10   | 52.93.12.255  |
| 38809 |   1608 | 52.93.12.169  | 52.93.13.83   |
| 40345 |   1677 | 100.64.16.173 | 52.95.30.217  |
| 40348 |   1677 | 52.95.31.18   | 27.0.0.248    |
| 40349 |   1677 | 27.0.0.248    | 54.239.41.161 |
| 40350 |   1677 | 54.239.41.161 | 54.239.43.132 |
| 40351 |   1677 | 54.239.43.132 | 52.93.13.10   |
| 40352 |   1677 | 52.93.13.10   | 52.93.12.255  |
| 40353 |   1677 | 52.93.12.255  | 52.93.12.146  |
| 43536 |   1803 | 52.95.31.131  | 52.95.31.18   |
| 43539 |   1803 | 54.239.41.161 | 54.239.43.132 |
| 43540 |   1803 | 54.239.43.132 | 52.93.13.10   |
| 43541 |   1803 | 52.93.13.10   | 52.93.12.255  |
| 43542 |   1803 | 52.93.12.255  | 52.93.12.146  |
| 43543 |   1803 | 52.93.12.146  | 52.93.12.169  |
| 43544 |   1803 | 52.93.12.169  | 52.93.13.83   |
| 43662 |   1808 | 100.64.16.173 | 52.95.30.217  |
| 43663 |   1808 | 52.95.30.217  | 52.95.31.131  |
| 43664 |   1808 | 52.95.31.131  | 52.95.31.18   |
| 43665 |   1808 | 52.95.31.18   | 27.0.0.248    |
| 43666 |   1808 | 27.0.0.248    | 54.239.41.161 |
| 43667 |   1808 | 54.239.41.161 | 54.239.43.132 |
| 43668 |   1808 | 54.239.43.132 | 52.93.13.10   |
| 43669 |   1808 | 52.93.13.10   | 52.93.12.255  |
| 43670 |   1808 | 52.93.12.255  | 52.93.12.146  |
| 43671 |   1808 | 52.93.12.146  | 52.93.12.169  |
| 43672 |   1808 | 52.93.12.169  | 52.93.13.83   |
| 47769 |   1977 | 100.64.16.173 | 52.95.30.217  |
| 47772 |   1977 | 52.95.30.217  | 52.95.31.131  |
| 47775 |   1977 | 52.95.31.131  | 52.95.31.18   |
| 47778 |   1977 | 52.95.31.18   | 27.0.0.248    |
| 47800 |   1977 | 52.93.12.169  | 52.93.13.83   |
| 47872 |   1980 | 100.64.16.173 | 52.95.30.217  |
| 47874 |   1980 | 52.95.30.217  | 52.95.31.131  |
| 47876 |   1980 | 52.95.31.131  | 52.95.31.18   |
| 47878 |   1980 | 52.95.31.18   | 27.0.0.248    |
| 47879 |   1980 | 27.0.0.248    | 54.239.41.161 |
| 47891 |   1980 | 52.93.12.169  | 52.93.13.83   |
| 47919 |   1982 | 100.64.16.173 | 52.95.30.217  |
| 47921 |   1982 | 52.95.30.217  | 52.95.31.131  |
| 47923 |   1982 | 52.95.31.131  | 52.95.31.18   |
| 47925 |   1982 | 52.95.31.18   | 27.0.0.248    |
| 47927 |   1982 | 27.0.0.248    | 54.239.41.161 |
| 47930 |   1982 | 54.239.41.161 | 54.239.43.132 |
| 47963 |   1984 | 100.64.16.173 | 52.95.30.217  |
| 47966 |   1984 | 52.95.30.217  | 52.95.31.131  |
| 47968 |   1984 | 52.95.31.131  | 52.95.31.18   |
| 47970 |   1984 | 52.95.31.18   | 27.0.0.248    |
| 47972 |   1984 | 27.0.0.248    | 54.239.41.161 |
| 47974 |   1984 | 54.239.41.161 | 54.239.43.132 |
| 49120 |   2031 | 100.64.16.173 | 52.95.30.217  |
| 49121 |   2031 | 52.95.30.217  | 52.95.31.131  |
| 49122 |   2031 | 52.95.31.131  | 52.95.31.18   |
| 49123 |   2031 | 52.95.31.18   | 27.0.0.248    |
| 49124 |   2031 | 27.0.0.248    | 54.239.41.161 |
| 49125 |   2031 | 54.239.41.161 | 54.239.43.132 |
| 49126 |   2031 | 54.239.43.132 | 52.93.13.10   |
| 49129 |   2031 | 52.93.12.146  | 52.93.12.169  |
| 49130 |   2031 | 52.93.12.169  | 52.93.13.83   |
| 52142 |   2152 | 52.95.31.131  | 52.95.31.18   |
| 52143 |   2152 | 52.95.31.18   | 27.0.0.248    |
| 52144 |   2152 | 27.0.0.248    | 54.239.41.161 |
| 52145 |   2152 | 54.239.41.161 | 54.239.43.132 |
| 52146 |   2152 | 54.239.43.132 | 52.93.13.10   |
| 52147 |   2152 | 52.93.13.10   | 52.93.12.255  |
| 52148 |   2152 | 52.93.12.255  | 52.93.12.146  |
| 52149 |   2152 | 52.93.12.146  | 52.93.12.169  |
| 52150 |   2152 | 52.93.12.169  | 52.93.13.83   |
+-------+--------+---------------+---------------+


CREATE TABLE trace6_with_3cables AS SELECT LatLng_trace6_with_3cables.id,lat,lng,idHop,idPath,ipSrc,ipDst FROM LatLng_trace6_with_3cables LEFT JOIN ip_trace6_with_3cables on LatLng_trace6_with_3cables.id=ip_trace6_with_3cables.id;

mysql> select * from trace6_with_3cables;
+-----+------------+--------------+-------+--------+---------------+---------------+
| id  | lat        | lng          | idHop | idPath | ipSrc         | ipDst         |
+-----+------------+--------------+-------+--------+---------------+---------------+
|   1 |  35.622094 |  139.7477703 |   642 |     33 | 100.64.16.173 | 52.95.30.217  |
|   2 | 39.3504015 |  147.4766443 |   646 |     33 | 52.95.30.217  | 52.95.31.131  |
|   3 | 42.5132741 |  156.0054677 |   649 |     33 | 52.95.31.131  | 52.95.31.18   |
|   4 | 45.3095116 |   165.180143 |   651 |     33 | 52.95.31.18   | 27.0.0.248    |
|   5 | 47.3282571 |  175.1544932 |   653 |     33 | 27.0.0.248    | 54.239.41.161 |
|   6 | 48.2652306 | -174.2500191 |   656 |     33 | 54.239.41.161 | 54.239.43.132 |
|   7 | 48.2053833 | -163.4721938 |   659 |     33 | 54.239.43.132 | 52.93.13.10   |
|   8 | 47.1583726 | -152.9231291 |   662 |     33 | 52.93.13.10   | 52.93.12.255  |
|   9 | 45.6247995 | -142.7552464 |   665 |     33 | 52.93.12.255  | 52.93.12.146  |
|  10 | 44.9547412 | -132.6992792 |   668 |     33 | 52.93.12.146  | 52.93.12.169  |
|  11 | 45.5320828 | -123.0053566 |   670 |     33 | 52.93.12.169  | 52.93.13.83   |
|  12 |  35.622094 |  139.7477703 |  1201 |     56 | 100.64.16.173 | 52.95.30.217  |
|  13 |  40.199048 |  149.5322349 |  1202 |     56 | 52.95.30.217  | 52.95.31.131  |
|  14 | 43.9671362 |  160.5049597 |  1208 |     56 | 27.0.0.248    | 54.239.41.161 |
|  15 | 46.9436978 |  172.5795178 |  1216 |     56 | 54.239.41.161 | 54.239.43.132 |
|  16 | 48.2652306 | -174.2500191 |  1225 |     56 | 54.239.43.132 | 52.93.13.10   |
|  17 | 48.0335711 | -160.7981512 |  1233 |     56 | 52.93.13.10   | 52.93.12.255  |
|  18 | 46.5043442 | -147.7675694 |  1239 |     56 | 52.93.12.255  | 52.93.12.146  |
|  19 | 45.0624263 | -135.2312851 |  1241 |     56 | 52.93.12.146  | 52.93.12.169  |
|  20 | 45.5320828 | -123.0053566 |  1243 |     56 | 52.93.12.169  | 52.93.13.83   |
|  21 |  35.622094 |  139.7477703 |  2288 |    105 | 100.64.16.173 | 52.95.30.217  |
|  22 | 41.5296498 |  153.0715847 |  2291 |    105 | 52.95.30.217  | 52.95.31.131  |
|  23 | 46.0946554 |  168.4142995 |  2295 |    105 | 52.95.31.131  | 52.95.31.18   |
|  24 | 48.2652306 | -174.2500191 |  2300 |    105 | 52.95.31.18   | 27.0.0.248    |
|  25 | 47.6108586 | -156.3908492 |  2305 |    105 | 27.0.0.248    | 54.239.41.161 |
|  26 | 45.1170786 | -139.4645287 |  2310 |    105 | 54.239.41.161 | 54.239.43.132 |
|  27 | 45.5320828 | -123.0053566 |  2332 |    105 | 52.93.12.169  | 52.93.13.83   |
|  28 |  35.622094 |  139.7477703 |  2475 |    114 | 100.64.16.173 | 52.95.30.217  |
|  29 | 30.9529134 |  153.2176012 |  2477 |    114 | 52.95.30.217  | 52.95.31.131  |
|  30 | 27.6047776 |   166.305162 |  2479 |    114 | 52.95.31.131  | 52.95.31.18   |
|  31 | 25.3805213 |  179.6880009 |  2481 |    114 | 52.95.31.18   | 27.0.0.248    |
|  32 |  23.198812 | -167.1908935 |  2483 |    114 | 27.0.0.248    | 54.239.41.161 |
|  33 | 22.5892236 | -154.4634196 |  2487 |    114 | 54.239.41.161 | 54.239.43.132 |
|  34 | 26.7199869 | -142.1966724 |  2495 |    114 | 52.93.12.255  | 52.93.12.146  |
|  35 | 35.9350664 |   -132.93662 |  2499 |    114 | 52.93.12.146  | 52.93.12.169  |
|  36 | 45.5320828 | -123.0053566 |  2502 |    114 | 52.93.12.169  | 52.93.13.83   |
|  37 |  35.622094 |  139.7477703 |  2536 |    117 | 100.64.16.173 | 52.95.30.217  |
|  38 | 30.9529134 |  153.2176012 |  2538 |    117 | 52.95.30.217  | 52.95.31.131  |
|  39 | 27.6047776 |   166.305162 |  2540 |    117 | 52.95.31.131  | 52.95.31.18   |
|  40 | 25.3805213 |  179.6880009 |  2542 |    117 | 52.95.31.18   | 27.0.0.248    |
|  41 |  23.198812 | -167.1908935 |  2544 |    117 | 27.0.0.248    | 54.239.41.161 |
|  42 | 22.5892236 | -154.4634196 |  2546 |    117 | 54.239.41.161 | 54.239.43.132 |
|  43 | 26.7199869 | -142.1966724 |  2547 |    117 | 54.239.43.132 | 52.93.13.10   |
|  44 | 35.9350664 |   -132.93662 |  2549 |    117 | 52.93.13.10   | 52.93.12.255  |
|  45 | 45.5320828 | -123.0053566 |  2555 |    117 | 52.93.12.169  | 52.93.13.83   |
|  46 |  35.622094 |  139.7477703 | 23749 |    994 | 100.64.16.173 | 52.95.30.217  |
|  47 | 29.0981737 |  157.3876906 | 23750 |    994 | 52.95.30.217  | 52.95.31.131  |
|  48 | 26.2601228 |  175.2862033 | 23752 |    994 | 52.95.31.131  | 52.95.31.18   |
|  49 |  23.198812 | -167.1908935 | 23754 |    994 | 52.95.31.18   | 27.0.0.248    |
|  50 | 23.7711329 | -150.2395426 | 23755 |    994 | 27.0.0.248    | 54.239.41.161 |
|  51 | 32.6786276 | -135.8446516 | 23756 |    994 | 54.239.41.161 | 54.239.43.132 |
|  52 | 45.5320828 | -123.0053566 | 23765 |    994 | 52.93.12.169  | 52.93.13.83   |
|  53 |  35.622094 |  139.7477703 | 23792 |    996 | 100.64.16.173 | 52.95.30.217  |
|  54 | 40.5291222 |   155.391978 | 23794 |    996 | 52.95.30.217  | 52.95.31.131  |
|  55 | 44.9107483 |  172.4012507 | 23796 |    996 | 52.95.31.131  | 52.95.31.18   |
|  56 | 46.3660548 | -168.7412529 | 23800 |    996 | 52.95.31.18   | 27.0.0.248    |
|  57 | 44.8072449 |  -149.923266 | 23803 |    996 | 27.0.0.248    | 54.239.41.161 |
|  58 | 42.9114557 |    -131.9527 | 23805 |    996 | 54.239.41.161 | 54.239.43.132 |
|  59 | 34.9001977 | -120.5404562 | 23814 |    996 | 52.93.12.146  | 52.93.12.169  |
|  60 | 45.5320828 | -123.0053566 | 23816 |    996 | 52.93.12.169  | 52.93.13.83   |
|  61 |  35.622094 |  139.7477703 | 24297 |   1017 | 100.64.16.173 | 52.95.30.217  |
|  62 | 40.0338925 |  153.3230658 | 24299 |   1017 | 52.95.30.217  | 52.95.31.131  |
|  63 | 43.9852895 |  167.9513253 | 24301 |   1017 | 52.95.31.131  | 52.95.31.18   |
|  64 | 46.1886754 | -175.9189199 | 24308 |   1017 | 54.239.41.161 | 54.239.43.132 |
|  65 | 45.9043392 | -159.2103911 | 24310 |   1017 | 54.239.43.132 | 52.93.13.10   |
|  66 | 43.7051117 | -143.1654078 | 24313 |   1017 | 52.93.13.10   | 52.93.12.255  |
|  67 | 42.5526007 | -127.4747969 | 24315 |   1017 | 52.93.12.255  | 52.93.12.146  |
|  68 | 35.5958125 | -122.3782042 | 24317 |   1017 | 52.93.12.146  | 52.93.12.169  |
|  69 | 45.5320828 | -123.0053566 | 24319 |   1017 | 52.93.12.169  | 52.93.13.83   |
|  70 |  35.622094 |  139.7477703 | 25473 |   1063 | 52.95.30.217  | 52.95.31.131  |
|  71 | 39.6235903 |  151.7352233 | 25474 |   1063 | 52.95.31.131  | 52.95.31.18   |
|  72 | 43.1493743 |  164.5923461 | 25475 |   1063 | 52.95.31.18   | 27.0.0.248    |
|  73 | 45.7430054 |  178.5642665 | 25476 |   1063 | 27.0.0.248    | 54.239.41.161 |
|  74 | 46.3321606 | -166.6116189 | 25477 |   1063 | 54.239.41.161 | 54.239.43.132 |
|  75 | 45.0557961 | -151.9703497 | 25478 |   1063 | 54.239.43.132 | 52.93.13.10   |
|  76 | 43.1153747 | -137.9802346 | 25479 |   1063 | 52.93.13.10   | 52.93.12.255  |
|  77 | 41.0566976 | -125.0269348 | 25480 |   1063 | 52.93.12.255  | 52.93.12.146  |
|  78 | 36.1172864 | -123.8293806 | 25481 |   1063 | 52.93.12.146  | 52.93.12.169  |
|  79 | 45.5320828 | -123.0053566 | 25482 |   1063 | 52.93.12.169  | 52.93.13.83   |
|  80 |  35.622094 |  139.7477703 | 30718 |   1272 | 100.64.16.173 | 52.95.30.217  |
|  81 |  40.199048 |  149.5322349 | 30719 |   1272 | 52.95.30.217  | 52.95.31.131  |
|  82 | 43.9671362 |  160.5049597 | 30720 |   1272 | 52.95.31.131  | 52.95.31.18   |
|  83 | 46.9436978 |  172.5795178 | 30721 |   1272 | 52.95.31.18   | 27.0.0.248    |
|  84 | 48.2652306 | -174.2500191 | 30722 |   1272 | 27.0.0.248    | 54.239.41.161 |
|  85 | 48.0335711 | -160.7981512 | 30723 |   1272 | 54.239.41.161 | 54.239.43.132 |
|  86 | 46.5043442 | -147.7675694 | 30724 |   1272 | 54.239.43.132 | 52.93.13.10   |
|  87 | 45.0624263 | -135.2312851 | 30725 |   1272 | 52.93.13.10   | 52.93.12.255  |
|  88 | 45.5320828 | -123.0053566 | 30726 |   1272 | 52.93.12.255  | 52.93.12.146  |
|  89 |  35.622094 |  139.7477703 | 31122 |   1289 | 100.64.16.173 | 52.95.30.217  |
|  90 |  40.199048 |  149.5322349 | 31123 |   1289 | 52.95.30.217  | 52.95.31.131  |
|  91 | 43.9671362 |  160.5049597 | 31124 |   1289 | 52.95.31.131  | 52.95.31.18   |
|  92 | 46.9436978 |  172.5795178 | 31125 |   1289 | 52.95.31.18   | 27.0.0.248    |
|  93 | 48.2652306 | -174.2500191 | 31128 |   1289 | 54.239.43.132 | 52.93.13.10   |
|  94 | 48.0335711 | -160.7981512 | 31129 |   1289 | 52.93.13.10   | 52.93.12.255  |
|  95 | 46.5043442 | -147.7675694 | 31130 |   1289 | 52.93.12.255  | 52.93.12.146  |
|  96 | 45.0624263 | -135.2312851 | 31131 |   1289 | 52.93.12.146  | 52.93.12.169  |
|  97 | 45.5320828 | -123.0053566 | 31132 |   1289 | 52.93.12.169  | 52.93.13.83   |
|  98 |  35.622094 |  139.7477703 | 38722 |   1604 | 100.64.16.173 | 52.95.30.217  |
|  99 | 42.5132741 |  156.0054677 | 38723 |   1604 | 52.95.30.217  | 52.95.31.131  |
| 100 | 47.3282571 |  175.1544932 | 38724 |   1604 | 52.95.31.131  | 52.95.31.18   |
| 101 | 48.2053833 | -163.4721938 | 38725 |   1604 | 52.95.31.18   | 27.0.0.248    |
| 102 | 45.6247995 | -142.7552464 | 38726 |   1604 | 27.0.0.248    | 54.239.41.161 |
| 103 | 45.5320828 | -123.0053566 | 38738 |   1604 | 52.93.12.169  | 52.93.13.83   |
| 104 |  35.622094 |  139.7477703 | 38777 |   1608 | 100.64.16.173 | 52.95.30.217  |
| 105 | 29.0981737 |  157.3876906 | 38781 |   1608 | 52.95.30.217  | 52.95.31.131  |
| 106 | 26.2601228 |  175.2862033 | 38784 |   1608 | 52.95.31.131  | 52.95.31.18   |
| 107 |  23.198812 | -167.1908935 | 38787 |   1608 | 52.95.31.18   | 27.0.0.248    |
| 108 | 23.7711329 | -150.2395426 | 38789 |   1608 | 27.0.0.248    | 54.239.41.161 |
| 109 | 32.6786276 | -135.8446516 | 38799 |   1608 | 52.93.13.10   | 52.93.12.255  |
| 110 | 45.5320828 | -123.0053566 | 38809 |   1608 | 52.93.12.169  | 52.93.13.83   |
| 111 |  35.622094 |  139.7477703 | 40345 |   1677 | 100.64.16.173 | 52.95.30.217  |
| 112 | 29.0981737 |  157.3876906 | 40348 |   1677 | 52.95.31.18   | 27.0.0.248    |
| 113 | 26.2601228 |  175.2862033 | 40349 |   1677 | 27.0.0.248    | 54.239.41.161 |
| 114 |  23.198812 | -167.1908935 | 40350 |   1677 | 54.239.41.161 | 54.239.43.132 |
| 115 | 23.7711329 | -150.2395426 | 40351 |   1677 | 54.239.43.132 | 52.93.13.10   |
| 116 | 32.6786276 | -135.8446516 | 40352 |   1677 | 52.93.13.10   | 52.93.12.255  |
| 117 | 45.5320828 | -123.0053566 | 40353 |   1677 | 52.93.12.255  | 52.93.12.146  |
| 118 |  35.622094 |  139.7477703 | 43536 |   1803 | 52.95.31.131  | 52.95.31.18   |
| 119 | 29.0981737 |  157.3876906 | 43539 |   1803 | 54.239.41.161 | 54.239.43.132 |
| 120 | 26.2601228 |  175.2862033 | 43540 |   1803 | 54.239.43.132 | 52.93.13.10   |
| 121 |  23.198812 | -167.1908935 | 43541 |   1803 | 52.93.13.10   | 52.93.12.255  |
| 122 | 23.7711329 | -150.2395426 | 43542 |   1803 | 52.93.12.255  | 52.93.12.146  |
| 123 | 32.6786276 | -135.8446516 | 43543 |   1803 | 52.93.12.146  | 52.93.12.169  |
| 124 | 45.5320828 | -123.0053566 | 43544 |   1803 | 52.93.12.169  | 52.93.13.83   |
| 125 |  35.622094 |  139.7477703 | 43662 |   1808 | 100.64.16.173 | 52.95.30.217  |
| 126 | 39.2799441 |  150.4787527 | 43663 |   1808 | 52.95.30.217  | 52.95.31.131  |
| 127 | 42.4116034 |  161.9738611 | 43664 |   1808 | 52.95.31.131  | 52.95.31.18   |
| 128 |  45.198358 |  174.2296684 | 43665 |   1808 | 52.95.31.18   | 27.0.0.248    |
| 129 | 46.3273714 | -172.5752946 | 43666 |   1808 | 27.0.0.248    | 54.239.41.161 |
| 130 | 45.9043392 | -159.2103911 | 43667 |   1808 | 54.239.41.161 | 54.239.43.132 |
| 131 | 44.2690027 | -146.2874129 | 43668 |   1808 | 54.239.43.132 | 52.93.13.10   |
| 132 | 43.0058255 | -133.7563233 | 43669 |   1808 | 52.93.13.10   | 52.93.12.255  |
| 133 | 39.3011827 |  -123.619777 | 43670 |   1808 | 52.93.12.255  | 52.93.12.146  |
| 134 | 36.9724482 | -124.4687919 | 43671 |   1808 | 52.93.12.146  | 52.93.12.169  |
| 135 | 45.5320828 | -123.0053566 | 43672 |   1808 | 52.93.12.169  | 52.93.13.83   |
| 136 |  35.622094 |  139.7477703 | 47769 |   1977 | 100.64.16.173 | 52.95.30.217  |
| 137 | 43.9852895 |  167.9513253 | 47772 |   1977 | 52.95.30.217  | 52.95.31.131  |
| 138 | 45.9043392 | -159.2103911 | 47775 |   1977 | 52.95.31.131  | 52.95.31.18   |
| 139 | 42.5526007 | -127.4747969 | 47778 |   1977 | 52.95.31.18   | 27.0.0.248    |
| 140 | 45.5320828 | -123.0053566 | 47800 |   1977 | 52.93.12.169  | 52.93.13.83   |
| 141 |  35.622094 |  139.7477703 | 47872 |   1980 | 100.64.16.173 | 52.95.30.217  |
| 142 | 42.4116034 |  161.9738611 | 47874 |   1980 | 52.95.30.217  | 52.95.31.131  |
| 143 | 46.3273714 | -172.5752946 | 47876 |   1980 | 52.95.31.131  | 52.95.31.18   |
| 144 | 44.2690027 | -146.2874129 | 47878 |   1980 | 52.95.31.18   | 27.0.0.248    |
| 145 | 39.3011827 |  -123.619777 | 47879 |   1980 | 27.0.0.248    | 54.239.41.161 |
| 146 | 45.5320828 | -123.0053566 | 47891 |   1980 | 52.93.12.169  | 52.93.13.83   |
| 147 |  35.622094 |  139.7477703 | 47919 |   1982 | 100.64.16.173 | 52.95.30.217  |
| 148 | 42.5132741 |  156.0054677 | 47921 |   1982 | 52.95.30.217  | 52.95.31.131  |
| 149 | 47.3282571 |  175.1544932 | 47923 |   1982 | 52.95.31.131  | 52.95.31.18   |
| 150 | 48.2053833 | -163.4721938 | 47925 |   1982 | 52.95.31.18   | 27.0.0.248    |
| 151 | 45.6247995 | -142.7552464 | 47927 |   1982 | 27.0.0.248    | 54.239.41.161 |
| 152 | 45.5320828 | -123.0053566 | 47930 |   1982 | 54.239.41.161 | 54.239.43.132 |
| 153 |  35.622094 |  139.7477703 | 47963 |   1984 | 100.64.16.173 | 52.95.30.217  |
| 154 | 28.1308127 |  160.8277289 | 47966 |   1984 | 52.95.30.217  | 52.95.31.131  |
| 155 | 24.7903846 | -177.7033451 | 47968 |   1984 | 52.95.31.131  | 52.95.31.18   |
| 156 | 21.8274654 | -156.9617255 | 47970 |   1984 | 52.95.31.18   | 27.0.0.248    |
| 157 | 30.3319801 |  -138.477002 | 47972 |   1984 | 27.0.0.248    | 54.239.41.161 |
| 158 | 45.5320828 | -123.0053566 | 47974 |   1984 | 54.239.41.161 | 54.239.43.132 |
| 159 |  35.622094 |  139.7477703 | 49120 |   2031 | 100.64.16.173 | 52.95.30.217  |
| 160 | 40.0338925 |  153.3230658 | 49121 |   2031 | 52.95.30.217  | 52.95.31.131  |
| 161 | 43.9852895 |  167.9513253 | 49122 |   2031 | 52.95.31.131  | 52.95.31.18   |
| 162 | 46.1886754 | -175.9189199 | 49123 |   2031 | 52.95.31.18   | 27.0.0.248    |
| 163 | 45.9043392 | -159.2103911 | 49124 |   2031 | 27.0.0.248    | 54.239.41.161 |
| 164 | 43.7051117 | -143.1654078 | 49125 |   2031 | 54.239.41.161 | 54.239.43.132 |
| 165 | 42.5526007 | -127.4747969 | 49126 |   2031 | 54.239.43.132 | 52.93.13.10   |
| 166 | 35.5958125 | -122.3782042 | 49129 |   2031 | 52.93.12.146  | 52.93.12.169  |
| 167 | 45.5320828 | -123.0053566 | 49130 |   2031 | 52.93.12.169  | 52.93.13.83   |
| 168 |  35.622094 |  139.7477703 | 52142 |   2152 | 52.95.31.131  | 52.95.31.18   |
| 169 |  40.199048 |  149.5322349 | 52143 |   2152 | 52.95.31.18   | 27.0.0.248    |
| 170 | 43.9671362 |  160.5049597 | 52144 |   2152 | 27.0.0.248    | 54.239.41.161 |
| 171 | 46.9436978 |  172.5795178 | 52145 |   2152 | 54.239.41.161 | 54.239.43.132 |
| 172 | 48.2652306 | -174.2500191 | 52146 |   2152 | 54.239.43.132 | 52.93.13.10   |
| 173 | 48.0335711 | -160.7981512 | 52147 |   2152 | 52.93.13.10   | 52.93.12.255  |
| 174 | 46.5043442 | -147.7675694 | 52148 |   2152 | 52.93.12.255  | 52.93.12.146  |
| 175 | 45.0624263 | -135.2312851 | 52149 |   2152 | 52.93.12.146  | 52.93.12.169  |
| 176 | 45.5320828 | -123.0053566 | 52150 |   2152 | 52.93.12.169  | 52.93.13.83   |
+-----+------------+--------------+-------+--------+---------------+---------------+
176 rows in set (0.00 sec)


mysql> 

// The table below will be retrived by curl commands using Google Elevation API.

// still need to modify it according table name
CREATE TEMPORARY TABLE 
IF NOT EXISTS table6_1_copy
AS select idPath,count(*) from ip_trace6_with_3cables GROUP BY idPath;
ALTER TABLE table6_1_copy ADD COLUMN id INT AUTO_INCREMENT NOT NULL, ADD primary key(id);

select * from table6_1_copy;

+--------+----------+----+
| idPath | count(*) | id |
+--------+----------+----+
|     33 |       11 |  1 |
|     56 |        9 |  2 |
|    105 |        7 |  3 |
|    114 |        9 |  4 |
|    117 |        9 |  5 |
|    994 |        7 |  6 |
|    996 |        8 |  7 |
|   1017 |        9 |  8 |
|   1063 |       10 |  9 |
|   1272 |        9 | 10 |
|   1289 |        9 | 11 |
|   1604 |        6 | 12 |
|   1608 |        7 | 13 |
|   1677 |        7 | 14 |
|   1803 |        7 | 15 |
|   1808 |       11 | 16 |
|   1977 |        5 | 17 |
|   1980 |        6 | 18 |
|   1982 |        6 | 19 |
|   1984 |        6 | 20 |
|   2031 |        9 | 21 |
|   2152 |        9 | 22 |
+--------+----------+----+
