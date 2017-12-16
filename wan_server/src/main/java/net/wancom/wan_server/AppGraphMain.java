package net.wancom.wan_server;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Dijkstra;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.json.JSONCountry;
import net.wancom.json.JSONLink;
import net.wancom.json.JSONNode;
import net.wancom.json.JSONUtil;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class AppGraphMain {
    public static void main(String[] args) {
        //TODO How to get each country as json ... solution?
        //We pretend that we get country name from somewhere and name it country. I use Scanner to test.
        Scanner keyboard = new Scanner(System.in);
        System.out.println("Let me know the country that you will trace a graph: ");
        String strCountry = keyboard.nextLine();
        System.out.println("What is the name of source you want to trace the graph from:");
        String source = keyboard.nextLine();
        try {
            JSONCountry country = JSONUtil.unmarshalJsonCountry(strCountry);
            Graph graph = createTheGraph(country);
            Node sourceNode = graph.findNode(source);
            if (sourceNode == null) {
                //TODO code should be better for UI :)
                System.out.println("The source is not in the graph. Try another source next time.");
                return;
            }
            graph = Dijkstra.calculateShortestPathFromSource(graph, sourceNode);

            System.out.println("Please enter your target to find the shortest path and cost: ");
            String target = keyboard.nextLine();
            Node targetNode = graph.findNode(target);
            if (targetNode == null) {
                //TODO code should be better for UI :)
                System.out.println("The target is not in the graph. Try another target next time.");
                return;
            }
            System.out.println("The shortest path's cost is " + targetNode.getCost());
            List<Node> shortestPath = targetNode.getShortestPath();
            String shortestPathAsString = shortestPath.stream ().map (node -> node.toString ()).collect (Collectors.joining ("-<<::>>-"));
            System.out.println("The shortest path is " + shortestPathAsString);
        } catch (WanComException we) {
            System.out.println("There is a problem (finding the file or parsing the json) and graph cannot be created: " + we.getMessage());
            we.printStackTrace();
        } catch (Exception e) {
            System.out.println("Something went wrong: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * The following method take json nodes and link and create all nodes of type(@see{{@link Node}}.
     * The initiated nodes has all neighbors as a list parameter in it.
     * The graph will be created and ready to run dijkstra algorithm.
     *
     * @param country the name of country you are going to create graph
     * @return the created graph ready to run dijkstra
     */
    public static Graph createTheGraph(JSONCountry country) {
        Graph graph = Graph.initGraph();
        List<JSONNode> jsonNodes = country.getNodes();
        List<JSONLink> jsonLinks = country.getLinks();

        if (jsonNodes == null || jsonNodes.isEmpty()) {
            throw new WanComException("The system cannot fetch any node from json file. Please control " + country + ".json first and run the application again.");
        }
        if (jsonLinks == null || jsonLinks.isEmpty()) {
            throw new WanComException("The system cannot fetch any link from json file. Please control " + country + ".json first and run the application again.");
        }

        List<Node> nodes = initializeAllNodes(jsonNodes, jsonLinks);
        if (nodes != null && !nodes.isEmpty()) {
            graph.addAllNodes(nodes);
        }

        return graph;
    }

    /**
     * TODO test the method before pushing
     * The method fills all nodes that is the neighbor of current node.
     * Return a list of node ready to create a graph.
     */
    private static List<Node> initializeAllNodes(List<JSONNode> jsonNodes, List<JSONLink> jsonLinks) {
        List<Node> nodes = new ArrayList<>();
        Iterator<JSONNode> jsonNodeIterator = jsonNodes.iterator();
        //initialize all nodes with longtitude and latitude and name.
        while (jsonNodeIterator.hasNext()) {
            JSONNode jsonNode = jsonNodeIterator.next();
            String jsonNodeId = jsonNode.getId();
            Node node = new Node(jsonNodeId);
            node.setLatitude(jsonNode.getLatitude());
            node.setLongtitude(jsonNode.getLongitude());
            node.setName(jsonNodeId);
            if (!nodes.contains(node)) {
                nodes.add(node);
            }
        }

        //We have to find all nearest adjacency of above node via link list we have
        // and fill immediateNeighborNodes
        Map<String, List<JSONLink>> jsonLinkWithSameSource
                = jsonLinks.stream().collect(Collectors.groupingBy(jl -> jl.getSource()));

        Iterator<String> allSource = jsonLinkWithSameSource.keySet().iterator();
        while (allSource.hasNext()) {
            String source = allSource.next();
            //We fetch the node that has source as nodeName (JSonNodeId)
            if (source != null) {
                Node sourceNode = nodes.stream().filter(n -> source.equals(n.getNodeName())).findFirst().orElse(null);
                if (sourceNode != null) {
                    List<JSONLink> jlinksWithJNodeIdAsSource = jsonLinkWithSameSource.get(source);
                    for (JSONLink jsonLink : jlinksWithJNodeIdAsSource) {
                        String target = jsonLink.getTarget();
                        if (target != null) {
                            Node adjacentNode = nodes.stream().filter(n -> target.equals(n.getNodeName())).findFirst().orElse(null);
                            if (adjacentNode != null) {
                                int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongtitude(),
                                        adjacentNode.getLatitude(), adjacentNode.getLongtitude());
                                sourceNode.addImmediateNeighborsDestination(adjacentNode, cost);
                            }
                        }
                    }
                }
            }
        }

        return nodes;
    }
}
