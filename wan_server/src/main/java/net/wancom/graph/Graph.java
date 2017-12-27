package net.wancom.graph;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
/**
 * We have a Graph that is a set of nodes.
 *
 * @see {@link Node}
 */
public class Graph {

    private Set<Node> nodes;

    private Graph() {
        this.nodes = new HashSet<>();
    }

    public static Graph initGraph() {
        return new Graph();
    }

    public void addNode(Node node) {
        nodes.add(node);
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
}
