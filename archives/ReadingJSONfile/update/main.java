import java.io.BufferedWriter;
import java.io.File;
import static java.io.FileDescriptor.in;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
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
        
        try {
            jsonObject = (JSONObject) parser.parse(new FileReader("/Users/biwen/Desktop/Uunet.json"));
            nodes = (JSONArray) jsonObject.get("nodes");
            links =(JSONArray) jsonObject.get("links") ;

            Map<String, JSONObject> mappedNodes = new HashMap<String, JSONObject>();
            File file = new File("/Users/biwen/Desktop/EdgeTest.txt"); //Your file

FileOutputStream fos = new FileOutputStream(file);

PrintStream ps = new PrintStream(fos);

System.setOut(ps);
 System.out.println( 42 );

            for (Object tmpNode : nodes){
                JSONObject tmpNode1 = (JSONObject) tmpNode;
                mappedNodes.put(tmpNode1.get("id").toString(), tmpNode1);
            }

            for(Object linkObj : links) {
                JSONObject link = (JSONObject) linkObj;
                JSONObject source = mappedNodes.get(link.get("source").toString());
                JSONObject target = mappedNodes.get(link.get("target").toString());
                
                double srcLatitude = Double.parseDouble(source.get("Latitude").toString());
                int Srcnum = (int) Double.parseDouble(target.get("num").toString());
                double srcLongitude = Double.parseDouble(source.get("Longitude").toString());
                
                double dstLatitude = Double.parseDouble(target.get("Latitude").toString());
                int dstnum = (int) Double.parseDouble(target.get("num").toString());
                double dstLongitude = Double.parseDouble(target.get("Longitude").toString());
                int  distance = (int) getDistance(srcLatitude, srcLongitude, dstLatitude, dstLongitude);
                int latecny =distance / 100;
                               
                System.out.println( (source.get("num")) + " " +(target.get("num")) + " " +latecny );

                 
                 
                 
             
                
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
    }}
