package net.wancom.graph;

import java.util.Iterator;
import java.util.List;

public class GraphUtil {


    /**
     * @param graph       The graph which the method will trace
     * @param source      source Node
     * @param destination destination Node
     * @return the shortest path between source and destination
     */
    public static List<Node> getShortestPathBetWeenTwoNodesInAGraph(Graph graph, Node source, Node destination) {
        List<Node> shortestPath = null;
        if (graph == null || source == null || destination == null) {
            return null;
        }
        Graph tracedGraph = Dijkstra.calculateShortestPathFromSource(graph, source);
        Iterator<Node> nodes = tracedGraph.getNodes().iterator();
        while (nodes.hasNext()) {
            Node node = nodes.next();
            if (destination.equals(node)) {
                return node.getShortestPath();
            }
        }
        return shortestPath;
    }

    /**
     * @param graph       The graph which the method will trace
     * @param source      source Node
     * @param destination destination Node
     * @return the minimum cost of two nodes
     */
    public static int getMinimumCostBetWeenTwoNodesInAGraph(Graph graph, Node source, Node destination) {
        int cost = 0;
        if (graph == null || source == null || destination == null) {
            return cost;
        }
        Graph tracedGraph = Dijkstra.calculateShortestPathFromSource(graph, source);
        Iterator<Node> nodes = tracedGraph.getNodes().iterator();
        while (nodes.hasNext()) {
            Node node = nodes.next();
            if (destination.equals(node)) {
                return node.getCost();
            }
        }
        return cost;
    }

    /**
     * The following method return the destination node that is filled with shortest path and cost from the source.
     *
     * @param graph       The graph which the method will trace
     * @param source      source Node
     * @param destination destination Node
     * @return destination node that has got shortestPath and cost filled.
     */
    public static Node getDestinationNodeWithInformation(Graph graph, Node source, Node destination) {
        if (graph == null || source == null || destination == null) {
            return null;
        }
        Graph tracedGraph = Dijkstra.calculateShortestPathFromSource(graph, source);
        Iterator<Node> nodes = tracedGraph.getNodes().iterator();
        while (nodes.hasNext()) {
            Node node = nodes.next();
            if (destination.equals(node)) {
                return node;
            }
        }
        return null;

    }


}
