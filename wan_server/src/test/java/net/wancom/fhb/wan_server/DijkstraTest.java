package net.wancom.fhb.wan_server;

import org.junit.Before;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class DijkstraTest {

    private Node nodeA;
    private Node nodeB;
    private Node nodeC;
    private Node nodeD;
    private Node nodeE;
    private Node nodeF;

    private Graph graph;

    //The following class runs before any test
    @Before
    public void init() {
        this.graph = initiateGraph();
    }


    @Test
    public void calculationTimeOfDijkstraAlgorithm() {
        long startTime = System.currentTimeMillis();
        Graph myGraph = getTracedGraphByDijkstra(nodeA);
        long stopTime = System.currentTimeMillis();
        long elapsedTime = stopTime - startTime;
        System.out.println("Elapsed time of running Dijkstra: " + elapsedTime + " miliseconds");
        assertNotNull(elapsedTime);

    }

    @Test
    public void calculateShortestPathFromSource() {
        Graph myGraph = getTracedGraphByDijkstra(nodeA);

        //Array.asList creates a list with the members in the paranthesis.
        //The following list has just one member nodeA
        List<Node> shortestPathForNodeB = Arrays.asList(nodeA);
        List<Node> shortestPathForNodeC = Arrays.asList(nodeA);

        //The following list has two members nodeA & nodeB
        List<Node> shortestPathForNodeD = Arrays.asList(nodeA, nodeB);

        //The following list has three members nodeA & nodeB & nodeD
        List<Node> shortestPathForNodeE = Arrays.asList(nodeA, nodeB, nodeD);
        List<Node> shortestPathForNodeF = Arrays.asList(nodeA, nodeB, nodeD);

        for (Node node : myGraph.getNodes()) {
            switch (node.getNodeName()) {
                case "B":
                    assertEquals(node.getShortestPath(), shortestPathForNodeB);
                    break;
                case "C":
                    assertEquals(node.getShortestPath(), shortestPathForNodeC);
                    break;
                case "D":
                    assertEquals(node.getShortestPath(), shortestPathForNodeD);
                    break;
                case "E":
                    assertEquals(node.getShortestPath(), shortestPathForNodeE);
                    break;
                case "F":
                    assertEquals(node.getShortestPath(), shortestPathForNodeF);
                    break;
            }
        }
    }

    private Graph getTracedGraphByDijkstra(Node source) {
        Graph tracedGraph = Dijkstra.calculateShortestPathFromSource(graph, source);
        return tracedGraph;
    }


    //Method prepared for init method.
    private Graph initiateGraph() {
        initializeNodes();

        nodeA.addImmediateNeighborsDestination(nodeB, 10);
        nodeA.addImmediateNeighborsDestination(nodeC, 15);

        nodeB.addImmediateNeighborsDestination(nodeD, 12);
        nodeB.addImmediateNeighborsDestination(nodeF, 15);

        nodeC.addImmediateNeighborsDestination(nodeE, 10);

        nodeD.addImmediateNeighborsDestination(nodeE, 2);
        nodeD.addImmediateNeighborsDestination(nodeF, 1);

        nodeF.addImmediateNeighborsDestination(nodeE, 5);

        Graph graph = Graph.initGraph();

        graph.addNode(nodeA);
        graph.addNode(nodeB);
        graph.addNode(nodeC);
        graph.addNode(nodeD);
        graph.addNode(nodeE);
        graph.addNode(nodeF);
        return graph;
    }

    private void initializeNodes() {
        this.nodeA = new Node("A");
        this.nodeB = new Node("B");
        this.nodeC = new Node("C");
        this.nodeD = new Node("D");
        this.nodeE = new Node("E");
        this.nodeF = new Node("F");
    }

}