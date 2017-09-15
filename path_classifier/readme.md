## Configuration

Path classifier requires **cluster.py**, a non git file, that is custom each host where path classifier is running and consistent among all instances.
Below you can see a sample of that file.
This file can be configured manually, or generated using az.py and custom config file (see az.py readme)

```python

cluster_conf.cluster = {
    'public_ips' : [
        {"ip" : "54.187.44.125", "end_node_name" : "CALI0", "id": -1},
        {"ip" : "52.57.153.194", "end_node_name" : "FRAN0", "id": -1}
        ],

    'our_public_ip' : "54.187.44.125",
    'our_private_ip' : "172.31.4.169",
    'our_index' : 0,
}
```

- **public_ips** list of dictionaries describing all instances that participate in path classification.
.. - **ip** public ip of each instance. I.e., if this instance of PC needs to send a message to a remote PC it will use this public IP information.
.. - **end_node_name** this is the name of the end node as stored in the MySQL database. Has to match the database for consistency.
.. - **id** This is unique ID as stored in MySQL, leave it blank. This value is populated automatically when PC connects to MySQL.
- **our_public_ip** self explanatory
- **our_private_ip** self explanatory
- **our_index** this is unique number for each host running PC, this is how we gain access to **public_ips** list and parameters stored in that list.



#### Performing ICMP measurements

This is a simple example of how to measure latency using ping and then convert it into a 2 column format for gnuplot use.

  - **ping 52.23.170.11 -i 0.2 -D > icmp.data**
  - **cat icmp.data | awk '{print $1 " " $8}' |  sed 's/[^0-9 ]*//g' > icmp.data.plot**


#### Performing TCP measurements

This is an example of using tcptracerout via tcpping script to perform TCP level pinging. Note, tcpping is a wrapper around tcptraceroute, all arguments passed to the wrapper are being redirected to tcptraceroute. See ''misc'' folder to get the modified version of the script that also print timestamps (existing limitation of the tcptraceroute).


  - **sudo ./tcpping 52.23.170.11 7000 -p 15000 > ./../tcp.data**
  - **cat tcp.data | awk '{print $1 " " $10}' > tcp.data**