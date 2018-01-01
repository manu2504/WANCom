package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import net.wancom.wan_server.SphericalGeometry;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import net.wancom.graph.*;
import net.wancom.json.JSONUtils;

public class NewGraph {
  
  /*
   * TODO: finish to write the function addBestNewNode(). This function requires:
   * (TODO) a function which evaluates the current total latency of a graph
   * (TODO) a function that adds a new node in a graph ( needs to use Graph.addNode() )
   * and after, a loop that iterates for all potential new nodes, and compute for each of them
   * the new total distance for the modified graph. This performance should be stored in a variable
   * that stores the best performance, and be replaced every time a better performance is found.
   */

    public static Graph addBestNewNode(Graph graph, String country, int constraint) throws FileNotFoundException, IOException {
        JSONObject jsonObject = JSONUtils.JSONObjectFromJSONFile(country);
        ArrayList<Node> oldnodes;
        JSONArray nodesList = (JSONArray) jsonObject.get("nodes");
        Map<String, Node> mapNodes = new HashMap<>();//not necessary
        oldnodes = (ArrayList<Node>) graph.getNodes();
        for (int i=0; i<nodesList.size();i++){
            JSONObject nodeObject = (JSONObject) nodesList.get(i);
            Node newNode = new Node("this newNode"+i);
            double nodeLat = Double.parseDouble(nodeObject.get("Latitude").toString());
            double nodeLong= Double.parseDouble(nodeObject.get("Longitude").toString());
            newNode.setLatitude(nodeLat);
            newNode.setLongitude(nodeLong);
            mapNodes.put("newNode" +i,newNode); //this might not be necessary
            graph.addNode(newNode); // this means that every nodes is in the graph

            for (int j =0; j<oldnodes.size();j++){
                Node sourceNode = oldnodes.get(j);
                int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongitude(),
                        newNode.getLatitude(), newNode.getLongitude());
                sourceNode.addImmediateNeighborsDestination(newNode, cost);
                newNode.addImmediateNeighborsDestination(sourceNode, cost);
                for(int x=j+1;x<oldnodes.size();x++){
                    Node targetNode = oldnodes.get(j);
                    int cost2 = SphericalGeometry.getDistance(targetNode.getLatitude(), targetNode.getLongitude(),
                            newNode.getLatitude(), newNode.getLongitude());
                    targetNode.addImmediateNeighborsDestination(newNode, cost2);
                    newNode.addImmediateNeighborsDestination(targetNode, cost2);
                    int totalCost= cost+cost2;
                    if(totalCost>constraint){
                            continue;
                    }

                   for (int y=0;y<oldnodes.size();x++){
                       Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
                   }
                   return graph;


                }


            }
        }
        return Graph.initGraph();
    }

}
