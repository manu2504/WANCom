package net.wancom.graph;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;


/**
 * Each Node in a graph will be an object of this class.
 */

public class Node {
    // Name of the Node
    private String nodeName;

    // The shortest path from the source Node (when we run Dijkstra algorith through a source)
    // to current Node - this (include all nodes between source and destination)
    private List<Node> shortestPath = new LinkedList<>();

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

    public List<Node> getShortestPath() {
        return shortestPath;
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

}
