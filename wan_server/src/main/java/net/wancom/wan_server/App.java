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
        //Graph g = graphFromJSONTopologies(jsonObject, Integer.valueOf(jsonObject.get("countryId").toString()));
        Graph g = graphFromJSONTopology(jsonObject);
        g.dijkstra(jsonObject.get("src").toString());
        shortestPath = g.printPath(jsonObject.get("dst").toString());
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
    List<Graph.Edge> GRAPH = new ArrayList<Graph.Edge>();
    JSONArray nodes_list = new JSONArray();
    JSONArray links_list = new JSONArray();
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
      double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
      double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
      double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
      double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
      int distance = SphericalGeometry.getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);

      GRAPH.add( j, new Graph.Edge(source.get("id").toString(), target.get("id").toString(), distance) );
      j++;
    }

    Graph g = new Graph(GRAPH);
    return g;
  }
}
