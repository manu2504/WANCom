package net.wancom.graph;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
/**
 * We have a Graph that is a set of nodes.
 *
 * @see {@link Node}
 *
 * Inspired by the implentation available at:
 * https://github.com/eugenp/tutorials/blob/master/algorithms/src/main/java/com/baeldung/algorithms/ga/dijkstra/Graph.java
 * authored by https://github.com/yasin3061
 */
public class Graph {

    private Set<Node> nodes;
    
    public String message; // to return info with the graph (BetterGraph.addBestNewNode uses it)

    private Graph() {
        this.nodes = new HashSet<>();
    }

    public static Graph initGraph() {
        return new Graph();
    }
    //add node to graph
    public void addNode(Node node) {
        nodes.add(node);
    }
    //remove node from graph
    public void removeNode(Node node){
        nodes.remove(node);
    }

    // getters and setters
    public Set<Node> getNodes() {
        return nodes;
    }

    public void setNodes(Set<Node> nodes) {
        this.nodes = nodes;
    }

    public Node findNode(String nodeName) {
        return this.nodes.stream().filter(n -> nodeName.equals(n.getNodeName())).findFirst().orElse(null);
    }

    public void addAllNodes(List<Node> nodes) {
        this.nodes = new HashSet<>(nodes);
    }
    
    public void resetCosts( ) {
        for (Node node : nodes) {
            node.setCost(Integer.MAX_VALUE);
        }
    }
}
