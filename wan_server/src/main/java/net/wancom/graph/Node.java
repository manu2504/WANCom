package net.wancom.graph;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;


/**
 * Each Node in a graph will be an object of this class.
 */

public class Node{
    // Name of the Node
    private String nodeName;
    private double longtitude;
    private double latitude;
    private String country;

    // The shortest path from the source Node (when we run Dijkstra algorithm through a source)
    // to current Node - this (include all nodes between source and destination)
    private List<Node> shortestPath = new LinkedList<>();
    
    // The javascript client expects a json response, so let's serve it json
    private JSONArray shortestPathAsJSONArray;

    //Distance between the node and source node, default value is the MAX_VALUE until we calcualte the real cost
    private Integer cost = Integer.MAX_VALUE;

    //immediateNeighborNodes is all immediate neighbors with cost (cost) to this node.
    Map<Node, Integer> immediateNeighborNodes = new HashMap<>();

    public void addImmediateNeighborsDestination(Node destination, int cost) {
        immediateNeighborNodes.put(destination, cost);
    }

    public Node(String nodeName) {
        this.nodeName = nodeName;
    }

    //Getters and Setters
    public String getNodeName() {
        return nodeName;
    }

    public void setName(String name) {
        this.nodeName = name;
    }

    public double getLongitude() {
        return longtitude;
    }

    public void setLongitude(double longtitude) {
        this.longtitude = longtitude;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public List<Node> getShortestPath() {
        return shortestPath;
    }
    
    @SuppressWarnings("unchecked")
    public JSONArray getShortestPathAsJSONArray() {
      shortestPathAsJSONArray = new JSONArray();
      for (Node elt : shortestPath) {
        shortestPathAsJSONArray.add(elt.getNodeName());
      }
      return shortestPathAsJSONArray;
    }

    public void setShortestPath(List<Node> shortestPath) {
        this.shortestPath = shortestPath;
    }
    
    public Integer getCost() {
        return cost;
    }

    public void setCost(Integer cost) {
        this.cost = cost;
    }

    public Map<Node, Integer> getImmediateNeighborNodes() {
        return immediateNeighborNodes;
    }

    public void setImmediateNeighborNodes(Map<Node, Integer> immediateNeighborNodes) {
        this.immediateNeighborNodes = immediateNeighborNodes;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Node)) return false;

        Node node = (Node) o;

        return getNodeName().equals(node.getNodeName());
    }

    @Override
    public String toString() {
        return "Node{" +
                "nodeName='" + nodeName + '\'' +
                ", longtitude=" + longtitude +
                ", latitude=" + latitude +
                ", cost=" + cost +
                '}';
    }
}
