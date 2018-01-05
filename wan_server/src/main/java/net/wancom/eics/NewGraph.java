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
import net.wancom.json.JSONUtils;

public class NewGraph {
  
  /*
   * TODO: finish to write the function addBestNewNode().
   * This function adds a new node in a graph ( needs to use Graph.addNode() )
   * and after, a loop that iterates for all potential new nodes, and compute for each of them
   * the new total distance for the modified graph. This performance should be stored in a variable
   * that stores the best performance, and be replaced every time a better performance is found.
   * 
   * 
   * (TODO) a function which evaluates the current total latency of a graph, needed by addBestNewNode (see below)
   */
    

    public static Graph addBestNewNode(Graph graph, String country, int constraint) throws FileNotFoundException, IOException {

        // For performance evaluation
        long startTimestamp = System.currentTimeMillis();
        long intermediateTimestamp; 
        long elapsedTime;
        
        // For notifying the user of the progress on the standard output
        int numberOfGraphsChecked = 0;
        int numberOfGraphsReallyEvaluated = 0;
        float percentage;

        JSONObject newTopology = JSONUtils.NewJSONTopologyFromJSONFile(country);
        List<Node> oldNodes = new ArrayList<>();
        JSONArray nodesList = (JSONArray) newTopology.get("nodes");
        System.out.println("No. of nodes in the initial graph: " + graph.getNodes().size());
        System.out.println("No. of new nodes: " + nodesList.size());
        int numberOfGraphsToBeEvaluated = nodesList.size() * ( (graph.getNodes().size() * (graph.getNodes().size() + 1) ) /2 );
        System.out.println("Estimated number of graphs to be evaluated: " + Integer.toString( numberOfGraphsToBeEvaluated ) );
        oldNodes.addAll(graph.getNodes());
        
        //List<Record> graphsPerformances = new ArrayList<>();
        Record bestRecord = new Record(null, null, Integer.MAX_VALUE);
        

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
            
            // Adding links to ONE new node (test pair-by-pair)
            for (int x = 0; x < oldNodes.size() - 1; x++) {
                Node oldNode1 = oldNodes.get(x);
                //System.out.println("oldNode1: " + oldNode1.getNodeName());
                int cost1 = Distance.getDistance(oldNode1.getLatitude(), oldNode1.getLongitude(),
                        newNode.getLatitude(), newNode.getLongitude());
                if (cost1 > constraint) {
                    numberOfGraphsChecked += oldNodes.size() - x;
                    continue;
                }
                oldNode1.addImmediateNeighborsDestination(newNode, cost1);
                newNode.addImmediateNeighborsDestination(oldNode1, cost1);
                for (int y = x + 1; y < oldNodes.size(); y++) {
                    Node oldNode2 = oldNodes.get(y);
                    if (oldNode2.equals(oldNode1)) {
                        System.err.println("Weird! There is a redundancy!");
                        continue;
                    }
                    //System.out.println("      oldNode2: " + oldNode2.getNodeName());
                    numberOfGraphsChecked++;
                    if ( numberOfGraphsChecked % (numberOfGraphsToBeEvaluated/1000) == 0 ) {
                        intermediateTimestamp = System.currentTimeMillis();
                        elapsedTime = intermediateTimestamp - startTimestamp;
                        percentage = (float) ((float) numberOfGraphsChecked*100.0f / (float) numberOfGraphsToBeEvaluated);
                        percentage = (float) (Math.round(percentage*100.0f)/100.0f);
                        System.out.println(numberOfGraphsChecked + "/" + numberOfGraphsToBeEvaluated + " graphs evaluated (" + Float.toString(percentage) + "%) - " + elapsedTime/(1000*60) + "min");
                    }
                    int cost2 = Distance.getDistance(oldNode2.getLatitude(), oldNode2.getLongitude(),
                            newNode.getLatitude(), newNode.getLongitude());
                    int totalCost = cost1 + cost2;
                    if (totalCost > constraint) {
                            continue;
                    }
                    numberOfGraphsReallyEvaluated++;
                   
                    oldNode2.addImmediateNeighborsDestination(newNode, cost2);
                    newNode.addImmediateNeighborsDestination(oldNode2, cost2);
                    
                    int totalDistance = computeTotalDistance(graph, oldNodes);
                    
                    // Building a set of neighbours (Node, cost) to add to the record
                    Map<Node, Integer> neighbours = new HashMap<>();
                    neighbours.put(oldNode1, cost1);
                    neighbours.put(oldNode2, cost2);
                    
                    
                    Record record = new Record(newNode, neighbours, totalDistance);
                    if (record.compareTo(bestRecord) < 0) {
                        //System.out.println("better distance found: " + Integer.toString(record.getTotalDistance()));
                        bestRecord = record;
                    }
                    //System.out.println("Added " + record.toString());
                    //graphsPerformances.add(record);
                    
                    oldNode2.removeImmediateNeighborsDestination(newNode);
                    newNode.removeImmediateNeighborsDestination(oldNode2);

                   //return graph;
                }
                oldNode1.removeImmediateNeighborsDestination(newNode);
                newNode.removeImmediateNeighborsDestination(oldNode1);
            }
            graph.removeNode(newNode);
        }
        
        //Record bestRecord = graphsPerformances.get(graphsPerformances.indexOf(Collections.min(graphsPerformances)));
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
     * Compute the sum of the distances between all pairs of nodes in the graph (we ignore the new nodes added when forming a pair)
     */
    private static int computeTotalDistance(Graph graph, List<Node> oldNodes) {
        int res = 0;
        for (int i = 0; i < oldNodes.size() - 1; i++) {
            Dijkstra.calculateShortestPathFromSource(graph, oldNodes.get(i));
            for (int j = i+1; j < oldNodes.size(); j++) {
                res += oldNodes.get(j).getCost();
            }
            graph.resetCosts(); // Needed to avoid that Dijsktra compare cost that correspond to a different source node and that are thus inaccurate
        }
        return res;
    }
    
    /*
     * for each graph: total distance. Store total distance in a hashMap <New node(s), new link(s), distance>
     * 
     */
    
    static class Record implements Comparable<Record> {
        private Node newNode;
        private Map<Node, Integer> neighbours;
        private int totalDistance;
        
        public Record(Node node, Map<Node, Integer> neighbours, int totalDistance) {
            this.newNode = node;
            this.neighbours = neighbours;
            this.totalDistance = totalDistance;
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
        public int getTotalDistance() {
            return totalDistance;
        }
        public void setTotalDistance(int totalDistance) {
            this.totalDistance = totalDistance;
        }
        
        @Override
        public int compareTo(Record other) {
            int res = -10;
            if (other.getTotalDistance() > this.getTotalDistance()) res = -1;
            if (other.getTotalDistance() == this.getTotalDistance()) res = 0;
            if (other.getTotalDistance() < this.getTotalDistance()) res = 1;
            if (res == -10) new WanComException("Damn! Records couldn't be compared to each other.");
            return res;
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
                    ", totalDistance= " + totalDistance +
                    " }";
        }
    }

}
