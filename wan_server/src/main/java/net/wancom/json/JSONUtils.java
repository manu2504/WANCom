package net.wancom.json;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.wan_server.SphericalGeometry;

public class JSONUtils {

    public static JSONObject JSONObjectFromJSONFile(String filename) throws FileNotFoundException, IOException {
        JSONParser parser = new JSONParser();
        JSONObject jsonObject = null;
        String path = getJSONFileFullName(filename);
        try {
            Object obj = parser.parse(new FileReader(path));
            jsonObject = (JSONObject) obj;
        } catch (ParseException e) {
            System.err.println("Parsing error");
        }
        return jsonObject;
    }

    public static JSONObject NewJSONTopologyFromJSONFile(String filename) throws FileNotFoundException, IOException {
        JSONParser parser = new JSONParser();
        JSONObject jsonObject = null;
        String path = getNewLocationsJSONFileFullName(filename);
        try {
            Object obj = parser.parse(new FileReader(path));
            jsonObject = (JSONObject) obj;
        } catch (ParseException e) {
            System.err.println("Parsing error");
        }
        return jsonObject;
    }

    public static String getJSONFileFullName(String filename) {
        // Class loader to find json files, there may exist another solution for this
        // part, the only goal is to find and read json files.
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        String path = classLoader.getResource("public/" + filename + ".json").getFile();
        return path;
    }

    public static String getNewLocationsJSONFileFullName(String filename) {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        String path = classLoader.getResource("public/new_locations/" + filename + ".json").getFile();
        return path;
    }

    public static File getJSONFile(String filename) {
        String path = getJSONFileFullName(filename);
        File jsonFile = new File(path);
        return jsonFile;
    }

    /*
     * Takes one of these topologies as a JSON object:
     * https://gits-15.sys.kth.se/iaq/WANCom/commit/
     * b434726fa46919c409ea1a2f1304fcb1b6535e62 And return a Graph object for
     * running Dijkstra against it
     */
    public static Graph graphFromJSONTopology(JSONObject jsonObject) {
        JSONArray nodesList;
        JSONArray linksList;
        List<Node> nodes;
        Map<String, Node> mapNodes = new HashMap<>();
        Graph graph = Graph.initGraph();

        nodesList = (JSONArray) jsonObject.get("nodes");
        linksList = (JSONArray) jsonObject.get("links");

        // START: add all the nodes to the graph
        for (Object tmpNode : nodesList) {
            JSONObject jsonTmpNode = (JSONObject) tmpNode;
            String nodeName = jsonTmpNode.get("id").toString();
            Node node = new Node(nodeName);
            double lat = Double.parseDouble(jsonTmpNode.get("latitude").toString());
            double lng = Double.parseDouble(jsonTmpNode.get("longitude").toString());
            String country = jsonTmpNode.get("country").toString();
            node.setLatitude(lat);
            node.setLongitude(lng);
            node.setCountry(country);
            mapNodes.put(nodeName, node);
        }
        // END: add all the nodes to the graph

        // START: add all the links to the graph
        for (Object linkObj : linksList) {
            JSONObject link = (JSONObject) linkObj;
            String sourceNodeName = link.get("source").toString();
            String destNodeName = link.get("target").toString();
            Node sourceNode = mapNodes.get(sourceNodeName);
            Node destNode = mapNodes.get(destNodeName);
            if (sourceNode == null || destNode == null) {
                throw new WanComException("Node not found!");
            }
            int cost = SphericalGeometry.getDistance(sourceNode.getLatitude(), sourceNode.getLongitude(),
                    destNode.getLatitude(), destNode.getLongitude());
            sourceNode.addImmediateNeighborsDestination(destNode, cost);
            destNode.addImmediateNeighborsDestination(sourceNode, cost);
            mapNodes.replace(sourceNodeName, sourceNode);
            mapNodes.replace(destNodeName, destNode);
        }
        // END: add all the links to the graph

        nodes = new ArrayList<>(mapNodes.values());

        graph.addAllNodes(nodes);
        return graph;
    }

    /*
     * Takes one of these topologies as a JSON object:
     * https://gits-15.sys.kth.se/iaq/WANCom/commit/
     * b434726fa46919c409ea1a2f1304fcb1b6535e62 And return a Graph object for
     * running Dijkstra against it
     */
    @SuppressWarnings("unchecked")
    public static JSONObject JSONTopologyFromGraph(Graph graph) {
        JSONObject jsonTopology = new JSONObject();
        JSONArray nodesList = new JSONArray();
        JSONArray linksList = new JSONArray();
        Set<Node> nodesSet;
        nodesSet = graph.getNodes();
        /*for (Node s : nodesSet) {
            System.out.println("node from new graph: " + s.toString());
        }*/
        // List<Node> nodes = new ArrayList<>(nodesSet);
        for (Node node : nodesSet) {
            JSONObject jsonNode = new JSONObject();
            double lat = node.getLatitude();
            double lng = node.getLongitude();
            String nodeName = node.getNodeName();
            String countryName = node.getCountry();
            Boolean isNewnode = node.getIsNewNode();
            Map<Node, Integer> immediateNeighborNodes = node.getImmediateNeighborNodes();
            System.out.println("nodename = "+nodeName);
            for (Map.Entry<Node, Integer> entry : immediateNeighborNodes.entrySet()) {
                System.out.println("neighbour nodename = "+entry.getKey().getNodeName());
                JSONObject jsonLink = new JSONObject();
                jsonLink.put("source", nodeName);
                jsonLink.put("target", entry.getKey().getNodeName());
                if (isNewnode || entry.getKey().getIsNewNode()) {
                    jsonLink.put("new", true);
                }
                //System.out.println("neighbour for " + nodeName + ": "+ entry.getKey().getNodeName());
                linksList.add(jsonLink);
            }
            //System.out.println("links list: "+linksList.toString());
            jsonNode.put("latitude", lat);
            jsonNode.put("longitude", lng);
            jsonNode.put("id", nodeName);
            jsonNode.put("country", countryName);
            jsonNode.put("new", isNewnode);
            nodesList.add(jsonNode);
        }
        jsonTopology.put("nodes", nodesList);
        jsonTopology.put("links", linksList);

        return jsonTopology;
    }
}
