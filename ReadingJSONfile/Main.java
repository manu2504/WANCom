
import java.io.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.json.simple.*;
import org.json.simple.parser.JSONParser;

public class Main {
    public static void main(String[] args) throws Exception {
        JSONParser parser = new JSONParser();
        JSONObject jsonObject;
        JSONArray nodes;
        JSONArray links;
// output the results to a text file
        PrintStream out= new PrintStream(new FileOutputStream("C:\\Users\\ibrah\\Desktop\\distance.txt"));

        try {
            jsonObject = (JSONObject) parser.parse(new FileReader("C:\\Users\\ibrah\\Desktop\\testJSON.json"));
            // save the results from reading nodes and links into a JSON arrays
            nodes = (JSONArray) jsonObject.get("nodes");
            links =(JSONArray) jsonObject.get("links") ;
            // create a map that has id as a key and json object
            Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();
            for (Object tmpNode : nodes){
                JSONObject tmpNode1 = (JSONObject) tmpNode;
                mappedNodes.put(tmpNode1.get("id").toString(), tmpNode1);
            }
            for(Object linkObj : links) {
                JSONObject link = (JSONObject) linkObj;
                JSONObject source = mappedNodes.get(link.get("source").toString());
                JSONObject target = mappedNodes.get(link.get("target").toString());
                double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
                double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
                double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
                double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
                double distance = getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);
                System.out.println("Distance between source " + source.get("id")+ " and destination " + target.get("id") + " is " + distance);
                out.print(source.get("id")+",");
                out.print(target.get("id")+ ",");
                out.println(distance);
            }
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static double getDistance(double lat1, double lon1, double lat2, double lon2) {
        double theta = lon1 - lon2;
        double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2)) + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos( degreeToRadiens(theta));
        dist = Math.acos(dist);
        dist =radiensTodegrees(dist);
        dist = dist * 60 * 1.1515;
        dist = dist * 1.609344;
        return (dist);
    }

    private static double degreeToRadiens(double degree) {
        return (degree * Math.PI / 180.0);
    }

    private static double radiensTodegrees(double radines) {
        return (radines * 180 / Math.PI);
    }
}
