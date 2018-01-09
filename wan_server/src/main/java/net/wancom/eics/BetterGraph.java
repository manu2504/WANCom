package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
//import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.*;
import net.wancom.json.Density;
import net.wancom.json.JSONUtils;

public class BetterGraph {
  
  /*
   * 
   */

    public static Graph addBestNewNode(Graph graph, String country, String sourceNodeName,
            String targetNodeName, int constraint, String accuracy) throws FileNotFoundException, IOException {

        // For performance evaluation
        long startTimestamp = System.currentTimeMillis();
        long intermediateTimestamp; 
        long elapsedTime;
        
        // For notifying the user of the progress on the standard output
        int numberOfGraphsChecked = 0;
        int numberOfGraphsReallyEvaluated = 0;
        int numberOfGraphsToBeEvaluated;
        float percentage;

        // We build a graph with the new topology
        Density density = null;
        switch (accuracy) {
        case "low":
            density = Density.LOW;
            break;
        case "middle":
            density = Density.MIDDLE;
            break;
        case "high":
            density = Density.HIGH;
            break;
        case "":
            throw new WanComException("Please specify the density for the mesh of new nodes");
        }
        JSONObject newTopology = JSONUtils.newJSONTopology(country, density);
        JSONArray newNodes = (JSONArray) newTopology.get("nodes");
        
        // Info to the standard output
        System.out.println("No. of nodes in the initial graph: " + graph.getNodes().size());
        System.out.println("No. of new nodes: " + newNodes.size());
        numberOfGraphsToBeEvaluated = newNodes.size() * ( ( (graph.getNodes().size() - 1) * graph.getNodes().size() ) /2);
        System.out.println("Estimated number of graphs to be evaluated: " + Integer.toString( numberOfGraphsToBeEvaluated ) );
        
        // Copy of all nodes in the current graph, to allow to create links with them
        // without being disturbed by new nodes added to the graph
        List<Node> oldNodes = new ArrayList<>();
        oldNodes.addAll(graph.getNodes());
        
        // We run Dijkstra on the current topology
        Node sourceNode = graph.findNode(sourceNodeName);
        Node targetNode = graph.findNode(targetNodeName);
        if (sourceNode == null ) {
            throw new WanComException("Source node '" + sourceNodeName + "' not found in the graph!");
        }
        if (targetNode == null) {
            throw new WanComException("Target node '" + targetNodeName + "' not found in the graph!");
        }

        Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
        
        // Here we keep a record of the length of the shortest path
        int bestDistanceOfShortestPath = targetNode.getCost();
        System.out.println("Current shortest path: "+Integer.toString(bestDistanceOfShortestPath)+" km");

        // Here we store the best new node with its neighbors
        Record bestRecord = new Record(null, null);
        
        // Add new nodes to the graph (try one-by-one)
        for (int i = 0; i < newNodes.size(); i++) {
            JSONObject nodeObject = (JSONObject) newNodes.get(i);
            Node newNode = new Node("New Node " + i);
            double nodeLat = Double.parseDouble(nodeObject.get("Latitude").toString());
            double nodeLong= Double.parseDouble(nodeObject.get("Longitude").toString());
            newNode.setLatitude(nodeLat);
            newNode.setLongitude(nodeLong);
            newNode.setCountry(country);
            newNode.setIsNewNode(true);
            graph.addNode(newNode);
            
            // Adding links to ONE new node (test pair-by-pair)
            for (int x = 0; x < oldNodes.size() - 1; x++) {
                Node oldNode1 = oldNodes.get(x);
                //System.out.println("oldNode1: " + oldNode1.getNodeName());
                int cost1 = Distance.getDistance(oldNode1.getLatitude(), oldNode1.getLongitude(),
                        newNode.getLatitude(), newNode.getLongitude());
                if (cost1 > constraint) {
                    numberOfGraphsChecked += oldNodes.size() - x - 1;
                    continue;
                }
                oldNode1.addImmediateNeighborsDestination(newNode, cost1);
                newNode.addImmediateNeighborsDestination(oldNode1, cost1);
                for (int y = x + 1; y < oldNodes.size(); y++) {
                    Node oldNode2 = oldNodes.get(y);
                    if (oldNode2.equals(oldNode1)) {
                        throw new WanComException("Weird! There is a redundancy!");
                    }
                    //System.out.println("      oldNode2: " + oldNode2.getNodeName());
                    numberOfGraphsChecked++;
                    if ( numberOfGraphsChecked % (numberOfGraphsToBeEvaluated/100) == 0) {
                        intermediateTimestamp = System.currentTimeMillis();
                        elapsedTime = intermediateTimestamp - startTimestamp;
                        percentage = (float) ((float) numberOfGraphsChecked*100.0f / (float) numberOfGraphsToBeEvaluated);
                        percentage = (float) (Math.round(percentage*100.0f)/100.0f);
                        System.out.println(numberOfGraphsChecked + "/" + numberOfGraphsToBeEvaluated + " graphs checked (" + Float.toString(percentage) + "%) - " + elapsedTime + "ms");
                    }
                    int cost2 = Distance.getDistance(oldNode2.getLatitude(), oldNode2.getLongitude(),
                            newNode.getLatitude(), newNode.getLongitude());
                    int totalCost = cost1 + cost2;
                    if (totalCost > constraint) {
                            continue;
                    }
                   
                    oldNode2.addImmediateNeighborsDestination(newNode, cost2);
                    newNode.addImmediateNeighborsDestination(oldNode2, cost2);
                                        
                    numberOfGraphsReallyEvaluated++;
                    if (numberOfGraphsReallyEvaluated % 1000 == 0) {
                        intermediateTimestamp = System.currentTimeMillis();
                        elapsedTime = intermediateTimestamp - startTimestamp;
                        System.out.println(Integer.toString(numberOfGraphsReallyEvaluated) + " graphs fully evaluated (in " + Float.toString(elapsedTime) + " ms.)");
                    }
                    
                    // Building a set of neighbours (Node, cost) to add to the record
                    Map<Node, Integer> neighbours = new HashMap<>();
                    neighbours.put(oldNode1, cost1);
                    neighbours.put(oldNode2, cost2);
                    
                    Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
                    int currentTotalDistance = targetNode.getCost();
                    if (currentTotalDistance < bestDistanceOfShortestPath) {
                        System.out.println("Shortest path improved: " + Integer.toString(bestDistanceOfShortestPath) + "km");
                        bestDistanceOfShortestPath = currentTotalDistance;
                        bestRecord = new Record(newNode, neighbours);
                        System.out.println("Added " + bestRecord.toString());
                    }
                    
                    graph.resetCosts(); // so that it makes sense to run Dijkstra gain
                    oldNode2.removeImmediateNeighborsDestination(newNode);
                    newNode.removeImmediateNeighborsDestination(oldNode2);
                }
                oldNode1.removeImmediateNeighborsDestination(newNode);
                newNode.removeImmediateNeighborsDestination(oldNode1);
            }
            graph.removeNode(newNode);
        }
        
        if (bestRecord.getNewNode() == null) {
            System.out.println("No improvement made to the graph");
            return null; // no improvement
        }
        Node newNode = bestRecord.getNewNode();
        graph.addNode(newNode);
        for (Node neighbour : bestRecord.getNeighbours().keySet()) {
            newNode.addImmediateNeighborsDestination(neighbour, bestRecord.getNeighbours().get(neighbour));
        }
        System.out.println("Number of graphs checked (including not meeting the constraint): " + Integer.toString(numberOfGraphsChecked));
        System.out.println("Number of graphs really evaluated: " + Integer.toString(numberOfGraphsReallyEvaluated));
        return graph;
    }
    
    /*
     * for each graph: total distance. Store total distance in a hashMap <New node(s), new link(s), distance>
     * 
     */
    
    static class Record {
        private Node newNode;
        private Map<Node, Integer> neighbours;
        
        public Record(Node node, Map<Node, Integer> neighbours) {
            this.newNode = node;
            this.neighbours = neighbours;
        }
        
        public Node getNewNode() {
            return newNode;
        }
        public void setNewNode(Node newNode) {
            this.newNode = newNode;
        }
        public Map<Node, Integer> getNeighbours() {
            return neighbours;
        }
        public void setNeighbours(Map<Node, Integer> neighbours) {
            this.neighbours = neighbours;
        }
        
        @Override
        public String toString() {
            String neighboursNames = "";
            for (Node neighbour : this.neighbours.keySet()) {
                if (neighboursNames != "") neighboursNames += ", ";
                neighboursNames += neighbour.getNodeName();
            }
            return "Record { sourceNode = " +
                    this.newNode.getNodeName() +
                    ", neighbours= " + neighboursNames +
                    " }";
        }
    }

}
