import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Main {
    private static Graph.Edge[] GRAPH;

    private static final String START = "z";
    private static final String END = "a";

    public static void main(String[] args) throws Exception{

        JSONParser parser = new JSONParser();
        JSONObject jsonObject;
        JSONArray nodes;
        JSONArray links;
        Map<String, Graph.Vertex> vertices = new HashMap<>();
        Set<String> allPlaces = new HashSet<String>();

        try{
            jsonObject = (JSONObject) parser.parse(new FileReader("C:\\Users\\ibrah\\Desktop\\UunetTest.json"));
            // save the results from reading nodes and links into a JSON arrays
            nodes = (JSONArray) jsonObject.get("nodes");
            links =(JSONArray) jsonObject.get("links") ;
            // create a map that has id as a key and json object
            Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();
            for (Object tmpNode : nodes){
                JSONObject tmpNode1 = (JSONObject) tmpNode;
                mappedNodes.put(tmpNode1.get("id").toString(), tmpNode1);
                // vertices.put(tmpNode1.get("id").toString(),new Vertex( Double.parseDouble(tmpNode1.get("Latitude").toString()),
                //       Double.parseDouble(tmpNode1.get("Longitude").toString()),
                //     tmpNode1.get("id").toString()));
            }

            GRAPH= new Graph.Edge[ links.size()];
            int i =0;
            for(Object linkObj : links) {

                JSONObject link = (JSONObject) linkObj;
                JSONObject source = mappedNodes.get(link.get("source").toString());
                JSONObject target = mappedNodes.get(link.get("target").toString());
                double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
                double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
                double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
                double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
                int distance = getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);
                allPlaces.add(source.get("id").toString());

                allPlaces.add( target.get("id").toString());

                GRAPH[i]= new Graph.Edge( source.get("id").toString(), target.get("id").toString(), distance);
                i++;
            }
           // System.out.println("here"+allPlaces);
            allPlaces.toArray();
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        Graph g = new Graph(GRAPH);
        for (String s: allPlaces) {
            g.dijkstra(s);
            g.printAllPaths();
        }
        }

    private static int getDistance(double lat1, double lon1, double lat2, double lon2) {
        double theta = lon1 - lon2;
        double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2)) + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos( degreeToRadiens(theta));
        dist = Math.acos(dist);
        dist =radiensTodegrees(dist);
        dist = dist * 60 * 1.1515;
        dist = dist * 1.609344;
        return (int)dist;
    }

    private static double degreeToRadiens(double degree) {
        return (degree * Math.PI / 180.0);
    }

    private static double radiensTodegrees(double radines) {
        return (radines * 180 / Math.PI);
    }
}


