package net.wancom;

import deprecated.algorithm.SphericalGeometry;
import net.wancom.exceptions.WanComException;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.json.JSONCountry;
import net.wancom.json.JSONLink;
import net.wancom.json.JSONNode;

import java.util.*;

public class GraphTestUtil {

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

    private static List<Node> initializeAllNodes(List<JSONNode> jsonNodes, List<JSONLink> jsonLinks) {
        List<Node> nodes = new ArrayList<>();
        Iterator<JSONNode> jsonNodeIterator = jsonNodes.iterator();
        //initialize all nodes with longtitude and latitude and name.
        while (jsonNodeIterator.hasNext()) {
            JSONNode jsonNode = jsonNodeIterator.next();
            String jsonNodeId = jsonNode.getId();
            Node node = new Node(jsonNodeId);
            node.setLatitude(jsonNode.getLatitude());
            node.setLongitude(jsonNode.getLongitude());
            node.setName(jsonNodeId);
            if (!nodes.contains(node)) {
                nodes.add(node);
            }
        }

        //We have to find all nearest adjacency of above node via link list we have
        // and fill immediateNeighborNodes
        Map<String, List<JSONLink>> jsonLinkWithSameSource
                = new HashMap<>();
        //        = jsonLinks.stream().collect(Collectors.groupingBy(jl -> jl.getSource()));

        Iterator<JSONLink> jsonLinksItr = jsonLinks.iterator();
        while (jsonLinksItr.hasNext()) {
            JSONLink jsonLink = jsonLinksItr.next();
            String source = jsonLink.getSource();
            String target = jsonLink.getTarget();
            putAdjacencyNode(jsonLinkWithSameSource, jsonLink, source);
            putAdjacencyNode(jsonLinkWithSameSource, jsonLink, target);
        }

        Iterator<String> allSource = jsonLinkWithSameSource.keySet().iterator();
        while (allSource.hasNext()) {
            String source = allSource.next();
            //We fetch the node that has source as nodeName (JSonNodeId)
            if (source != null) {
                Node sourceNode = nodes.stream().filter(n -> source.equals(n.getNodeName())).findFirst().orElse(null);
                if (sourceNode != null) {
                    List<JSONLink> jLinksWithJNodeIdAsSource = jsonLinkWithSameSource.get(source);
                    for (JSONLink jsonLink : jLinksWithJNodeIdAsSource) {
                        String target1 = jsonLink.getTarget();
                        if (!source.equals(target1)) {
                            calculateAdjacencyNodesCost(nodes, sourceNode, target1);
                        }
                        String target2 = jsonLink.getSource();
                        if (!source.equals(target2)) {
                            calculateAdjacencyNodesCost(nodes, sourceNode, target2);
                        }

                    }
                }
            }
        }

        return nodes;
    }

    private static void calculateAdjacencyNodesCost(List<Node> nodes, Node sourceNode, String target) {
        if (target != null) {
            Node adjacentNode = nodes.stream().filter(n -> target.equals(n.getNodeName())).findFirst().orElse(null);
            if (adjacentNode != null) {
                int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongitude(),
                        adjacentNode.getLatitude(), adjacentNode.getLongitude());
                sourceNode.addImmediateNeighborsDestination(adjacentNode, cost);
            }
        }
    }

    private static void putAdjacencyNode(Map<String, List<JSONLink>> jsonLinkWithSameSource, JSONLink jsonLink, String sourceName) {
        if (jsonLinkWithSameSource.containsKey(sourceName) &&
                !jsonLinkWithSameSource.get(sourceName).contains(jsonLink)) {
            jsonLinkWithSameSource.get(sourceName).add(jsonLink);
        } else if (!jsonLinkWithSameSource.containsKey(sourceName)) {
            List<JSONLink> links = new ArrayList<>();
            links.add(jsonLink);
            jsonLinkWithSameSource.put(sourceName, links);
        }
    }

}
