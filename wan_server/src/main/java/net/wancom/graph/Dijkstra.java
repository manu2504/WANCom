package net.wancom.graph;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.Map.Entry;
import java.util.Set;

public class Dijkstra {


    /**
     * Dijkstra algorithm:
     * The following algorithm, get a source and calculate the shortest path to other nodes of graph.
     * After running, the grap's Node get two parameters initiated: shortestPath from source
     * and cost that is the lowest cost from source to the node. So to get the shortest path between two nodes,
     * we should run the following method and use one of the two nodes as source, and then from the other node
     * get shortestPath and cost.
     * @param graph
     *              The graph that we will trace from a node to another one
     * @param source
     * @return
     */

    public static Graph calculateShortestPathFromSource(Graph graph, Node source) {
        source.setCost(0);

        Set<Node> settledNodes = new HashSet<>();
        Set<Node> unsettledNodes = new HashSet<>();

        unsettledNodes.add(source);

        while (unsettledNodes.size() != 0) {
            Node currentNode = getLowestCostNode(unsettledNodes);
            unsettledNodes.remove(currentNode);
            for (Entry<Node, Integer> adjacencyPair :
                    currentNode.getImmediateNeighborNodes().entrySet()) {
                Node adjacentNode = adjacencyPair.getKey();
                Integer edgeWeight = adjacencyPair.getValue();
                if (!settledNodes.contains(adjacentNode)) {
                    calculateCostEffectiveMinimumDistance(adjacentNode, edgeWeight, currentNode);
                    unsettledNodes.add(adjacentNode);
                }
            }
            settledNodes.add(currentNode);
        }
        return graph;
    }

    private static Node getLowestCostNode(Set<Node> unsettledNodes) {
        Node lowestDistanceNode = null;
        int lowestDistance = Integer.MAX_VALUE;
        for (Node node : unsettledNodes) {
            int nodeDistance = node.getCost();
            if (nodeDistance < lowestDistance) {
                lowestDistance = nodeDistance;
                lowestDistanceNode = node;
            }
        }
        return lowestDistanceNode;
    }

    private static void calculateCostEffectiveMinimumDistance(Node evaluationNode,
                                                              Integer edgeCost, Node sourceNode) {
        Integer sourceCost = sourceNode.getCost();
        if (sourceCost + edgeCost < evaluationNode.getCost()) {
            evaluationNode.setCost(sourceCost + edgeCost);
            LinkedList<Node> shortestPath = new LinkedList<>(sourceNode.getShortestPath());
            if (shortestPath.isEmpty()) {
              shortestPath.add(sourceNode);
            }
            shortestPath.add(evaluationNode);
            evaluationNode.setShortestPath(shortestPath);
        }
    }
}
