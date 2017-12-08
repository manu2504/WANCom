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
    IntersectionPoint.test();
    
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
      // return "{ \"lat\": 123.0, \"lng\": 146.0 }";
      return shortestPath;
    }, new JsonTransformer());
  }

  /*
   * private JSONObject shortestPathFromJSONTopology(JSONObject topo, String src,
   * String target) { return new JSONObject(); }
   */
  private static Graph graphFromJSONTopology(JSONObject jsonObject, int graphId) {
    List<List<Graph.Edge>> GRAPHS = new ArrayList<List<Graph.Edge>>();
    //JSONArray nodes;
    //JSONArray links;
    //Set<String> allPlaces = new HashSet<String>();

    JSONArray[] nodess = new JSONArray[5];
    JSONArray[] linkss = new JSONArray[5];
    List<Map<String, JSONObject>> mappedNodess = new ArrayList<Map<String, JSONObject>>();
    for (int i = 0; i < 5; i++) {
      nodess[i] = (JSONArray) jsonObject.get("nodes" + Integer.toString(i+1) );
      linkss[i] = (JSONArray) jsonObject.get("links" + Integer.toString(i+1) );
      mappedNodess.add(i, new HashMap<String, JSONObject>());
    }
    /*
    nodes = (JSONArray) jsonObject.get("nodes");
    links = (JSONArray) jsonObject.get("links");
    // create a map that has id as a key and json object
    Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();*/
    for (int i = 0; i < 5; i++) {
      for (Object tmpNode : nodess[i]) {
        JSONObject tmpNode1 = (JSONObject) tmpNode;
        mappedNodess.get(i).put(tmpNode1.get("id").toString(), tmpNode1);
      }
    }

    for (int i = 0; i < 5; i++) {
      GRAPHS.add( i, new ArrayList<Graph.Edge>(linkss[i].size()) );
    }
    for (int j = 0; j < 5; j++) {
      int i = 0;
      for (Object linkObj : linkss[j]) {
  
        JSONObject link = (JSONObject) linkObj;
        JSONObject source = mappedNodess.get(j).get(link.get("source").toString());
        JSONObject target = mappedNodess.get(j).get(link.get("target").toString());
        double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
        double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
        double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
        double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
        int distance = getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);
        //allPlaces.add(source.get("id").toString());
  
        //allPlaces.add(target.get("id").toString());
  
        GRAPHS.get(j).add( i, new Graph.Edge(source.get("id").toString(), target.get("id").toString(), distance) );
        i++;
      }
    }
    //System.out.println("here"+allPlaces);
    //allPlaces.toArray();

    Graph g = new Graph(GRAPHS.get(graphId-1));
    return g;
  }

  private static int getDistance(double lat1, double lon1, double lat2, double lon2) {
    double theta = lon1 - lon2;
    double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2))
        + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos(degreeToRadiens(theta));
    dist = Math.acos(dist);
    dist = radiensTodegrees(dist);
    dist = dist * 60 * 1.1515;
    dist = dist * 1.609344;
    return (int) dist;
  }

  private static double degreeToRadiens(double degree) {
    return (degree * Math.PI / 180.0);
  }

  private static double radiensTodegrees(double radines) {
    return (radines * 180 / Math.PI);
  }
}
