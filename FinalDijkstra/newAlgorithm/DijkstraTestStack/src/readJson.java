import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
/*
public class readJson {
    private static Graph.Edge[] GRAPH;
    public static void main(String[] args) throws Exception {
        JSONParser parser = new JSONParser();
        JSONObject jsonObject;
        JSONArray nodes;

        Map<String, Graph.Vertex> vertices = new HashMap<>();

        try {
            jsonObject = (JSONObject) parser.parse(new FileReader("C:\\Users\\ibrah\\Desktop\\data_USA.json"));
            // save the results from reading nodes and links into a JSON arrays
            nodes = (JSONArray) jsonObject.get("nodes");
            // create a map that has id as a key and json object
            ArrayList<JSONObject> nodesList = new ArrayList<>();
            Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();
            for (Object tmpNode : nodes) {
                JSONObject tmpNode1 = (JSONObject) tmpNode;
                nodesList.add(tmpNode1);

            }
            GRAPH= new Graph.Edge[ nodesList.size()];
            for (int i =0; i < nodesList.size();i++){
               JSONObject source = nodesList.get(i);
               double srclat= Double.parseDouble(source.get("Latitude").toString());
               double srclong= Double.parseDouble(source.get("Longitude").toString());
                System.out.println(source);
                System.out.println("Latitude: " + srclat);
                System.out.println("Longitude :" + srclong);
                for(int j=i+1;j<nodesList.size();j++){
                    JSONObject target = nodesList.get(j);
                    double dstlat =Double.parseDouble( target.get("Latitude").toString());
                    double dstlong= Double.parseDouble(target.get("Longitude").toString());

                    int distance = getDistance(srclat, srclong, dstlat, dstlong);
                    System.out.println("Distance between " + " sourcelat " + nodesList.get(i).get("Latitude").toString() + " sourcelong " + nodesList.get(i).get("Longitude").toString() + "----- and destination -----> "
                            + " destinationlat " + nodesList.get(j).get("Latitude").toString()  + " Destinationlong " + nodesList.get(j).get("Longitude").toString() +" ------ " + distance);


                    mappedNodes.put("node"+i+""+j,target);

                    System.out.println(mappedNodes);

                  //  GRAPH[j]= new Graph.Edge( , , distance);
                }

            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static int getDistance(double lat1, double lon1, double lat2, double lon2) {
        double theta = lon1 - lon2;
        double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2)) + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos(degreeToRadiens(theta));
        dist = Math.acos(dist);
        dist = radiensTodegrees(dist);
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
*/