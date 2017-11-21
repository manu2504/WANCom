
// combine all path.xml for the trace:

cat trace6_1.xml trace6_2.xml trace6_3.xml trace6_4.xml trace6_5.xml trace6_6.xml trace6_7.xml trace6_8.xml trace6_9.xml trace6_10.xml trace6_11.xml trace6_12.xml trace6_13.xml trace6_14.xml trace6_15.xml trace6_16.xml trace6_17.xml trace6_18.xml trace6_19.xml trace6_20.xml trace6_21.xml trace6_22.xml > trace6_all.xml


CREATE TABLE `LatLng_trace6_all` (
  `lat` double  NULL ,
  `lng` double  NULL 
);


LOAD XML LOCAL INFILE '/Users/vv/Desktop/all_traces_in_4_datacenter/Trace6/request_results_from_Elevation_API/trace6_all.xml' 
INTO TABLE LatLng_trace6_all rows identified by '<location>';

