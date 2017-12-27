The **purpose of this project** is to build and **interactive tool** able to suggest topology improvements in Wide Area Networks. The goal is to improve average end-to-end latency between any pair of nodes in the network.

During the first phase of this project, we analyzed data retrieved from measurements (produced by traceroute) performed among multiple geo-distributed datacenters of Amazon EC2.

What we could analyze, is that the network latency is closely related to the geographical distance.

Our goal has thus been to design an **Expert Change Infrastructure System (EICS)** that suggests network topology improvements by suggesting new nodes to add to the network.

To achieve it, we collected data from open-source GML datasets containing the national network topologies for five countries (USA, Finland, China, Germany, France).

We then converted this GML data to JSON and displayed it onto a world map (using Google Maps).

Our expert system has several entry parameters:
1. the number of new nodes that can be added into the network
2. the maximal distance of the new links that can be added into the network

**The EICS is based on the following algorithm:**
1. Compute the current total latency between all pair of nodes in the studied network topology, by running Dijkstra's algorithm for each pair of nodes.
2. Generate a list of locations where a new node could be added in the national network topology. This list is generated based on a fixed distance between each location.
3. For each potential candidate location, add a node to the network with this location, and,
4.1 for any two nodes in the graph, create a link to this new node if it respects the constraint (ie. the maximum distance allowed for new links - the distance already used for previous new nodes added to the network), then compute the new total distance for any pair of nodes in the graph, by running the Dijkstra's algorithm for each of them. Store this value if it is better than the previously-computed ones, along with the new node's location and the total distances of new links added.
5. At the end of step 2, we have the best new potential location for a new node; the EICS adds it to the network.
6. Repeat steps 2 and 3 for how many new nodes have been requested.
7. The network is returned to the user with network improvements highlighted on the map (and distances' improvements given to the user)

# Running the server
Our client-side visualization tool is served by the server, whereas the EICS is run on the server side. The server is written in Java. You thus need to have Java 8 installed on your machine.
## Open the wan_server Java project
Open from your favorite Java IDE the project whose root is wan_server (at the root of the folder).
The server should be running at localhost:4567

You can now use the visualisation tool as follows:
1. From there, you can zoom on one network topology, eg. USA, and select two nodes.
2. Then, behind the world map, the dashboard allows you to request the shortest path between these two nodes.
3. You can see the result of Dijkstra's algorithm displayed on the map.
4. Now comes into play the EICS. You can request an improved graph, after having selected how many new nodes can be added to this new graph, and selected what is the maximum distance allowed for new links added to the network.

An other feature could be how precise is the step between two potential locations, in order to be able to make more accurate choices for the new nodes.

# Help
To get set up with git and the code review tool we used, cf. "GIT & CR setups.md"
