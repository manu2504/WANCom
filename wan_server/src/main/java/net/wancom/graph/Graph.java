package net.wancom.graph;

import java.util.HashSet;
import java.util.Set;

/**
 * We have a Graph that is a set of nodes.
 * @see {@link Node}
 */
public class Graph {

    private Set<Node> nodes;

    private Graph(){
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

    public Node findNode(String nodeName){
        if(!hasNode(nodeName)){
            return null;
        }
        return this.getNodes().stream().filter(node -> nodeName.equals(node.getNodeName())).findFirst().orElse(null);
    }

    public boolean hasNode(String nodeName){
        if(nodeName==null || !this.getNodes().contains(new Node(nodeName))){
            return false;
        }
        return true;
    }
}
