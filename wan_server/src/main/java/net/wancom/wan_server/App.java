package net.wancom.wan_server;

import static spark.Spark.*;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Dijkstra;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;


/**
 * Main class from which the server is run
 */
public class App {
 
  public static void main(String[] args) throws FileNotFoundException, IOException {
    staticFiles.location("/public"); // Static files
    get("/hello", (request, response) -> "Hello guys!");
    System.out.println("Server listening on port 4567");
    
    post("/senddata", (request, response) -> {
      System.out.println("data received: " + request.body());

      JSONParser parser = new JSONParser();
      JSONArray shortestPath = null;

      try {
        Object obj = parser.parse(request.body());
        JSONObject jsonObject = (JSONObject) obj;
        Graph graph = graphFromJSONTopology(jsonObject);
        Node sourceNode = graph.findNode(jsonObject.get("src").toString());
        if (sourceNode == null) {
          //How should application handle when user inserts a source not available!
          throw new WanComException("Source is not in the graph!");
        }
        graph = Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
        Node targetNode = graph.findNode(jsonObject.get("dst").toString());
        if (targetNode == null) {
          //How should application handle when user inserts a target not available!
          throw new WanComException("Target is not in the graph!");
        }

        shortestPath = targetNode.getShortestPathAsJSONArray();
        System.out.println("Shortest path: " + ((JSONArray) shortestPath).toString());
      } catch (ParseException e) {
        System.err.println("Parsing error");
      }
      return shortestPath;
    });
  }


  /*
   * Takes one of these topologies as a JSON object:
   * https://gits-15.sys.kth.se/iaq/WANCom/commit/b434726fa46919c409ea1a2f1304fcb1b6535e62
   * And return a Graph object for running Dijkstra against it
   */
  private static Graph graphFromJSONTopology(JSONObject jsonObject) {
    JSONArray nodesList;
    JSONArray linksList;
    List<Node> nodes;
    Map<String, Node> mapNodes = new HashMap<>();
    Graph graph = Graph.initGraph();

    nodesList = (JSONArray) jsonObject.get("nodes");
    linksList = (JSONArray) jsonObject.get("links");

    // START: add all the nodes to the graph
    for (Object tmpNode : nodesList) {
      JSONObject jsonTmpNode = (JSONObject) tmpNode;
      String nodeName = jsonTmpNode.get("id").toString();
      Node node = new Node(nodeName);
      double lat = Double.parseDouble(jsonTmpNode.get("latitude").toString());
      double lng = Double.parseDouble(jsonTmpNode.get("longitude").toString());
      node.setLatitude(lat);
      node.setLongitude(lng);
      mapNodes.put(nodeName, node);
    }
    // END: add all the nodes to the graph

    // START: add all the links to the graph
    for (Object linkObj : linksList) {
      JSONObject link = (JSONObject) linkObj;
      String sourceNodeName = link.get("source").toString();
      String destNodeName = link.get("target").toString();
      Node sourceNode = mapNodes.get(sourceNodeName);
      Node destNode = mapNodes.get(destNodeName);
      if (sourceNode == null || destNode == null) {
        throw new WanComException("Node not found!");
      }
      int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongitude(),
          destNode.getLatitude(), destNode.getLongitude());
      sourceNode.addImmediateNeighborsDestination(destNode, cost);
      destNode.addImmediateNeighborsDestination(sourceNode, cost);
      mapNodes.replace(sourceNodeName, sourceNode);
      mapNodes.replace(destNodeName, destNode);
    }
    // END: add all the links to the graph
    
    nodes = new ArrayList<>(mapNodes.values());
    
    graph.addAllNodes(nodes);
    return graph;
  }
  /* Implementation used for Ibra's implementation (deprecated.Graph)
  private static Graph graphFromJSONTopology(JSONObject jsonObject) {
    List<Graph.Edge> GRAPH = new ArrayList<Graph.Edge>();
    JSONArray nodes_list;
    JSONArray links_list;
    Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();

    nodes_list = (JSONArray) jsonObject.get("nodes");
    links_list = (JSONArray) jsonObject.get("links");

    for (Object tmpNode : nodes_list) {
      JSONObject tmpNode1 = (JSONObject) tmpNode;
      mappedNodes.put(tmpNode1.get("id").toString(), tmpNode1);
    }

    int j = 0;
    for (Object linkObj : links_list) {
      JSONObject link = (JSONObject) linkObj;
      JSONObject source = mappedNodes.get(link.get("source").toString());
      JSONObject target = mappedNodes.get(link.get("target").toString());
      double srcLatitude = Double.parseDouble(source.get("latitude").toString());
      double srcLongitude = Double.parseDouble(source.get("longitude").toString());
      double dstLatitude = Double.parseDouble(target.get("latitude").toString());
      double dstLongitude = Double.parseDouble(target.get("longitude").toString());
      int distance = SphericalGeometry.getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);

      GRAPH.add( j, new Graph.Edge(source.get("id").toString(), target.get("id").toString(), distance) );
      j++;
    }

    Graph g = new Graph(GRAPH);
    return g;
  }*/
}
