package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

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
        JSONObject jsonObject = JSONUtils.NewJSONTopologyFromJSONFile(country);
        Set<Node> oldNodes = new HashSet<>();
        JSONArray nodesList = (JSONArray) jsonObject.get("nodes");
        oldNodes.addAll(graph.getNodes());

        // Add new nodes to the graph (try one-by-one)
        for (int i = 0; i < nodesList.size(); i++) {
            JSONObject nodeObject = (JSONObject) nodesList.get(i);
            Node newNode = new Node("newNode"+i);
            double nodeLat = Double.parseDouble(nodeObject.get("Latitude").toString());
            double nodeLong= Double.parseDouble(nodeObject.get("Longitude").toString());
            newNode.setLatitude(nodeLat);
            newNode.setLongitude(nodeLong);
            newNode.setCountry(country);
            newNode.setIsNewNode(true);
            graph.addNode(newNode);
            
            // Adding links to the new node (test pair-by-pair)
            for (Node oldNode1 : oldNodes) {
                //System.out.println("iteration oldNode1: "+oldNode1.getNodeName());
                int cost1 = SphericalGeometry.getDistance(oldNode1.getLatitude(), oldNode1.getLongitude(),
                        newNode.getLatitude(), newNode.getLongitude());
                if (cost1 > constraint) continue;
                oldNode1.addImmediateNeighborsDestination(newNode, cost1);
                newNode.addImmediateNeighborsDestination(oldNode1, cost1);
                for (Node oldNode2 : oldNodes) {
                    //System.out.println("iteration oldNode2 "+oldNode2.getNodeName());
                    if (oldNode2.equals(oldNode1)) continue;
                    int cost2 = SphericalGeometry.getDistance(oldNode2.getLatitude(), oldNode2.getLongitude(),
                            newNode.getLatitude(), newNode.getLongitude());
                    int totalCost = cost1 + cost2;
                    if (totalCost > constraint) {
                            continue;
                    }
                   
                    oldNode2.addImmediateNeighborsDestination(newNode, cost2);
                    newNode.addImmediateNeighborsDestination(oldNode2, cost2);

                    for (int y = 0; y < oldNodes.size(); y++) {
                        Dijkstra.calculateShortestPathFromSource(graph, oldNode1);
                        //computeTotalDistance
                    }
                   //returning the graph here will give us single link from the new node to specific nodes that meet the constraint
                   return graph;
                }
                //returning the graph here will give us multiple links from the new node to all other nodes
                //return graph
                oldNode1.removeImmediateNeighborsDestination(newNode);
                newNode.removeImmediateNeighborsDestination(oldNode1);
            }
            graph.removeNode(newNode);
        }
        return null;
    }

}
