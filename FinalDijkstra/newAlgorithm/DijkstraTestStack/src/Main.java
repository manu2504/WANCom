import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Main {
    private static Graph.Edge[] GRAPH;
    private static Graph.Edge[] NEWGRAPH;
    public static void main(String[] args) throws Exception{
        JSONParser parser = new JSONParser();
        JSONObject jsonObject;
        JSONArray nodes;
        JSONArray nodes1;
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

            jsonObject = (JSONObject) parser.parse(new FileReader("C:\\Users\\ibrah\\Desktop\\data_USA.json"));
            // save the results from reading nodes into a JSON arrays
            nodes1 = (JSONArray) jsonObject.get("nodes");
            ArrayList<JSONObject> nodesList = new ArrayList<>();
            Map<String, JSONObject> mappedNodes1 = new HashMap<String, JSONObject>();
            for (Object tmpNode : nodes1) {
                JSONObject tmpNode1 = (JSONObject) tmpNode;
                nodesList.add(tmpNode1);

            }
            NEWGRAPH = new Graph.Edge[(int)Math.pow(nodesList.size(),2)];
            for (int i =0; i < nodesList.size();i++){
                JSONObject source = nodesList.get(i);
                double srclat= Double.parseDouble(source.get("Latitude").toString());
                double srclong= Double.parseDouble(source.get("Longitude").toString());
               // System.out.println(source);
               // System.out.println("Latitude: " + srclat);
                //System.out.println("Longitude :" + srclong);
                for(int j=i+1;j<nodesList.size();j++){
                    JSONObject target = nodesList.get(j);
                    double dstlat =Double.parseDouble( target.get("Latitude").toString());
                    double dstlong= Double.parseDouble(target.get("Longitude").toString());
                    int distance = getDistance(srclat, srclong, dstlat, dstlong);

                   // System.out.println("Distance between " + " sourcelat " + nodesList.get(i).get("Latitude").toString() + " sourcelong " + nodesList.get(i).get("Longitude").toString() + "----- and destination -----> "
                     //       + " destinationlat " + nodesList.get(j).get("Latitude").toString()  + " Destinationlong " + nodesList.get(j).get("Longitude").toString() +" ------ " + distance);

                   // mappedNodes1.put("node"+i+""+j,target);
                    allPlaces.add(source.toString());
                    allPlaces.add(target.toString());
                    NEWGRAPH[j]= new Graph.Edge(source.toString(),target.toString(),distance);
                }
            }

             allPlaces.toArray();
/*
            GRAPH = new Graph.Edge[links.size()];
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
            allPlaces.toArray();*/

        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

       /*
        Scanner in = new Scanner(System.in);
        String srcNode;
        String dstNode;
        System.out.print("choose a source node: ");
        srcNode= in.nextLine();

        System.out.print("choose a destination node: ");
        dstNode= in.nextLine();

        Graph g = new Graph(GRAPH);
        g.dijkstra(srcNode);
        g.printPath(dstNode);
*/
        Graph g = new Graph(NEWGRAPH);
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