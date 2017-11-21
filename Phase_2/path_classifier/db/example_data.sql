-- Insert some example data
INSERT INTO `tec`.`EndNodes` (`ip`, `name`) VALUES ('192.168.0.1', 'Sun');
INSERT INTO `tec`.`EndNodes` (`ip`, `name`) VALUES ('192.168.0.2', 'Venus');
INSERT INTO `tec`.`EndNodes` (`ip`, `name`) VALUES ('192.168.0.3', 'Mars');
INSERT INTO `tec`.`EndNodes` (`ip`, `name`) VALUES ('192.168.0.4', 'Earth');

-- Insert class paths
INSERT INTO `tec`.`TraceDirections` (`idTraceDirection`,`idSrc`, `idDst`) VALUES (1, 1, 3);
INSERT INTO `tec`.`TraceDirections` (`idTraceDirection`,`idSrc`, `idDst`) VALUES (2, 1, 4);
INSERT INTO `tec`.`TraceDirections` (`idTraceDirection`,`idSrc`, `idDst`) VALUES (3, 2, 4);
INSERT INTO `tec`.`TraceDirections` (`idTraceDirection`,`idSrc`, `idDst`) VALUES (4, 4, 1);

-- Insert some random path
-- There is only one path between node 1 and 3
INSERT INTO `tec`.`Paths` (`idPath`, `idTraceDirection`) VALUES (1, 1);
-- There are two paths between node 1 and 4
INSERT INTO `tec`.`Paths` (`idPath`, `idTraceDirection`) VALUES (2, 2);
INSERT INTO `tec`.`Paths` (`idPath`, `idTraceDirection`) VALUES (3, 2);

INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(1, 1, '192.168.0.14', '192.168.0.25', NULL);
INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(2, 1, '192.168.0.25', '192.168.0.13', 1);

INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(3, 2, '192.168.0.11', '192.168.0.142', NULL);
INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(4, 2, '192.168.0.142', '192.168.0.39', 3);
INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(5, 2, '192.168.0.39', '192.168.0.41', 4);

INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(6, 3, '192.168.0.34', '192.168.0.28', NULL);
INSERT INTO `tec`.`Hops`(`idHop`,`idPath`,`ipSrc`,`ipDst`, `idPredecessor`) VALUES(7, 3, '192.168.0.28', '192.168.0.36', 6);

-- Insert measurements for different paths
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(1, 53);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(1, 51);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(1, 49);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(1, 62);

INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(2, 153);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(2, 91);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(2, 148);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(2, 141);

INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(3, 76);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(3, 77);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(3, 74);
INSERT INTO `tec`.`Measurements` (`idPath`, `latency`) VALUES(3, 71);
