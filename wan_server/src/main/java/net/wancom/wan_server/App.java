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
 * Hello world!
 *
 */
public class App {
 
  public static void main(String[] args) throws FileNotFoundException, IOException {
    staticFiles.location("/public"); // Static files
    get("/hello", (request, response) -> "Hello guys!");
    System.out.println("Server listening on port 4567");

    // launching the function to find the point of intersection between
    // a circle and a curve
    SphericalGeometry.intersectionPoint();
    
    /*
    JSONParser parser = new JSONParser();
    try {
      Object obj = parser.parse(new FileReader("C:\\Users\\manuc\\Desktop\\test.json"));
      JSONObject jsonObject = (JSONObject) obj;
      System.out.println(jsonObject);
      Graph g = graphFromJSONTopology(jsonObject, 1);
      g.dijkstra("Vancouver");
      JSONArray ja = g.printPath("Boston");
      System.out.println(ja);
    } catch (ParseException e) {
      System.err.println("Parsing error");
    }*/
    post("/senddata", (request, response) -> {
      System.out.println("data received: " + request.body());

      JSONParser parser = new JSONParser();
      JSONArray shortestPath = null;
      try {
        Object obj = parser.parse(request.body());
        JSONObject jsonObject = (JSONObject) obj;
        Graph g = graphFromJSONTopology(jsonObject, Integer.valueOf(jsonObject.get("countryId").toString()));
        g.dijkstra(jsonObject.get("src").toString());
        shortestPath = g.printPath(jsonObject.get("dst").toString());
      } catch (ParseException e) {
        System.err.println("Parsing error");
      }
      return shortestPath;
    });
  }

  /*
   * Takes this topology as a JSON object:
   * https://gits-15.sys.kth.se/iaq/WANCom/blob/master/wan_server/src/main/resources/public/All_countries.js
   * And return a Graph object for running Dijkstra against it
   */
  private static Graph graphFromJSONTopology(JSONObject jsonObject, int graphId) {
    int topology_length = 5;
    List<List<Graph.Edge>> GRAPHS = new ArrayList<List<Graph.Edge>>();
    JSONArray[] nodes_lists = new JSONArray[topology_length];
    JSONArray[] links_lists = new JSONArray[topology_length];
    List<Map<String, JSONObject>> mappedNodes = new ArrayList<Map<String, JSONObject>>();
    
    // The topologies are numbered from 1 to 5 
    for (int i = 0; i < topology_length; i++) {
      nodes_lists[i] = (JSONArray) jsonObject.get("nodes" + Integer.toString(i+1) );
      links_lists[i] = (JSONArray) jsonObject.get("links" + Integer.toString(i+1) );
      mappedNodes.add(i, new HashMap<String, JSONObject>());
    }

    for (int i = 0; i < topology_length; i++) {
      for (Object tmpNode : nodes_lists[i]) {
        JSONObject tmpNode1 = (JSONObject) tmpNode;
        mappedNodes.get(i).put(tmpNode1.get("id").toString(), tmpNode1);
      }
    }

    for (int i = 0; i < topology_length; i++) {
      GRAPHS.add( i, new ArrayList<Graph.Edge>(links_lists[i].size()) );
    }
    for (int i = 0; i < topology_length; i++) {
      int j = 0;
      for (Object linkObj : links_lists[i]) {
        JSONObject link = (JSONObject) linkObj;
        JSONObject source = mappedNodes.get(i).get(link.get("source").toString());
        JSONObject target = mappedNodes.get(i).get(link.get("target").toString());
        double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
        double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
        double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
        double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
        int distance = SphericalGeometry.getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);
  
        GRAPHS.get(i).add( j, new Graph.Edge(source.get("id").toString(), target.get("id").toString(), distance) );
        j++;
      }
    }

    Graph g = new Graph(GRAPHS.get(graphId-1));
    return g;
  }
}
