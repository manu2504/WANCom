package net.wancom.wan_server;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Dijkstra;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.json.JSONCountry;
import net.wancom.json.JSONLink;
import net.wancom.json.JSONNode;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import static spark.Spark.*;


/**
 * Main class from which the server is run
 */
public class App {
 
  public static void main(String[] args) throws IOException {
    staticFiles.location("/public"); // Static files
    get("/hello", (request, response) -> "Hello guys!");
    System.out.println("Server listening on port 4567");
    post("/senddata", (request, response) -> {
      System.out.println("data received: " + request.body());

      JSONParser parser = new JSONParser();
      //JSONArray shortestPath = null;
      //Maybe we need to cast the list below to json compatible data type before we return it.
      List<Node> shortestPath = null;
      try {
        Object obj = parser.parse(request.body());
        JSONObject jsonObject = (JSONObject) obj;
        //Graph g = graphFromJSONTopologies(jsonObject, Integer.valueOf(jsonObject.get("countryId").toString()));
        Graph graph = graphFromJSONTopology(jsonObject);
        Node sourceNode = graph.findNode(jsonObject.get("src").toString());
        if (sourceNode == null) {
          //How should application handle when user inserts a source not available!
          throw new WanComException("Source is not in the graph");
        }
        graph = Dijkstra.calculateShortestPathFromSource(graph, sourceNode);

        Node targetNode = graph.findNode(jsonObject.get("dst").toString());
        if (sourceNode == null) {
          //How should application handle when user inserts a target not available!
          throw new WanComException("Target is not in the graph");
        }
        shortestPath = targetNode.getShortestPath();
        //shortestPath = g.printPath(jsonObject.get("dst").toString());
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
    JSONCountry country = new JSONCountry();
    JSONArray nodesList;
    List<JSONNode> jsonNodes = new ArrayList<>();
    JSONArray linksList;
    List<JSONLink> jsonLinks = new ArrayList<>();

    nodesList = (JSONArray) jsonObject.get("nodes");
    linksList = (JSONArray) jsonObject.get("links");

    //START: Create the list of nodes and set the country's node
    for (Object tmpNode : nodesList) {
      JSONObject jsonTmpNode = (JSONObject) tmpNode;
      JSONNode jsonNode = new JSONNode();
      jsonNode.setId(jsonTmpNode.get("id").toString());
      jsonNode.setLongitude(Double.parseDouble(jsonTmpNode.get("Longitude").toString()));
      jsonNode.setLatitude(Double.parseDouble(jsonTmpNode.get("Latitude").toString()));
      jsonNodes.add(jsonNode);
    }
    country.setNodes(jsonNodes);
    //END: Create the list of nodes and set the country's node


    //START: Create the list of links and set the country's links
    for (Object linkObj : linksList) {
      JSONObject link = (JSONObject) linkObj;
      JSONLink jsonLink = new JSONLink();
      jsonLink.setSource(link.get("source").toString());
      jsonLink.setTarget(link.get("target").toString());
      jsonLinks.add(jsonLink);
    }
    country.setLinks(jsonLinks);
    //END: Create the list of links and set the country's links

    Graph g = createTheGraph(country);
    return g;
  }

  /**
   * The following method take json nodes and link and create all nodes of type(@see{{@link Node}}.
   * The initiated nodes has all neighbors as a list parameter in it.
   * The graph will be created and ready to run dijkstra algorithm.
   *
   * @param country the name of country you are going to create graph
   * @return the created graph ready to run dijkstra
   */
  public static Graph createTheGraph(JSONCountry country) {
    Graph graph = Graph.initGraph();
    List<JSONNode> jsonNodes = country.getNodes();
    List<JSONLink> jsonLinks = country.getLinks();

    if (jsonNodes == null || jsonNodes.isEmpty()) {
      throw new WanComException("The system cannot fetch any node from json file. Please control " + country + ".json first and run the application again.");
    }
    if (jsonLinks == null || jsonLinks.isEmpty()) {
      throw new WanComException("The system cannot fetch any link from json file. Please control " + country + ".json first and run the application again.");
    }

    List<Node> nodes = initializeAllNodes(jsonNodes, jsonLinks);
    if (nodes != null && !nodes.isEmpty()) {
      graph.addAllNodes(nodes);
    }

    return graph;
  }

  /**
   * TODO test the method before pushing
   * The method fills all nodes that is the neighbor of current node.
   * Return a list of node ready to create a graph.
   */
  private static List<Node> initializeAllNodes(List<JSONNode> jsonNodes, List<JSONLink> jsonLinks) {
    List<Node> nodes = new ArrayList<>();
    Iterator<JSONNode> jsonNodeIterator = jsonNodes.iterator();
    //initialize all nodes with longtitude and latitude and name.
    while (jsonNodeIterator.hasNext()) {
      JSONNode jsonNode = jsonNodeIterator.next();
      String jsonNodeId = jsonNode.getId();
      Node node = new Node(jsonNodeId);
      node.setLatitude(jsonNode.getLatitude());
      node.setLongtitude(jsonNode.getLongitude());
      node.setName(jsonNodeId);
      if (!nodes.contains(node)) {
        nodes.add(node);
      }
    }

    //We have to find all nearest adjacency of above node via link list we have
    // and fill immediateNeighborNodes
    Map<String, List<JSONLink>> jsonLinkWithSameSource
            = jsonLinks.stream().collect(Collectors.groupingBy(jl -> jl.getSource()));

    Iterator<String> allSource = jsonLinkWithSameSource.keySet().iterator();
    while (allSource.hasNext()) {
      String source = allSource.next();
      //We fetch the node that has source as nodeName (JSonNodeId)
      if (source != null) {
        Node sourceNode = nodes.stream().filter(n -> source.equals(n.getNodeName())).findFirst().orElse(null);
        if (sourceNode != null) {
          List<JSONLink> jlinksWithJNodeIdAsSource = jsonLinkWithSameSource.get(source);
          for (JSONLink jsonLink : jlinksWithJNodeIdAsSource) {
            String target = jsonLink.getTarget();
            if (target != null) {
              Node adjacentNode = nodes.stream().filter(n -> target.equals(n.getNodeName())).findFirst().orElse(null);
              if (adjacentNode != null) {
                int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongtitude(),
                        adjacentNode.getLatitude(), adjacentNode.getLongtitude());
                sourceNode.addImmediateNeighborsDestination(adjacentNode, cost);
              }
            }
          }
        }
      }
    }

    return nodes;
  }

}