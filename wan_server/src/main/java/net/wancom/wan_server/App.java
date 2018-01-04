package net.wancom.wan_server;

import static spark.Spark.*;

import net.wancom.eics.NewGraph;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Dijkstra;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.json.JSONUtils;

/**
 * Main class from which the server is run
 */
public class App {

    public static void main(String[] args) {
        staticFiles.location("/public"); // Static files
        get("/hello", (request, response) -> "Hello guys!");
        System.out.println("Server listening on port 4567");

        post("/shortestpath", (request, response) -> {
            System.out.println("data received: " + request.body());

            JSONParser parser = new JSONParser();
            JSONArray shortestPath = null;

            try {
                Object obj = parser.parse(request.body());
                JSONObject jsonObject = (JSONObject) obj;
                String countryName = jsonObject.get("country").toString();

                JSONObject jsonTopology = JSONUtils.JSONObjectFromJSONFile(countryName);                
                Graph graph = JSONUtils.graphFromJSONTopology(jsonTopology);
                String sourceNodeName = jsonObject.get("src").toString();
                Node sourceNode = graph.findNode(sourceNodeName);
                if (sourceNode == null) {
                    // How should application handle when user inserts a source not available!
                    throw new WanComException("Source is not in the graph!");
                }
                graph = Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
                Node targetNode = graph.findNode(jsonObject.get("dst").toString());
                if (targetNode == null) {
                    // How should application handle when user inserts a target not available!
                    throw new WanComException("Target is not in the graph!");
                }

                shortestPath = targetNode.getShortestPathAsJSONArray();
                System.out.println("Shortest path: " + ((JSONArray) shortestPath).toString());
            } catch (ParseException e) {
                System.err.println("Parsing error");
            } catch (WanComException e) {
                System.err.println(e.getMessage());
            }

            return shortestPath;
        });

        post("/newgraph", (request, response) -> {
            System.out.println("data received: " + request.body());

            JSONParser parser = new JSONParser();
            JSONObject jsonResponse = null;

            try {
                Object obj = parser.parse(request.body());
                JSONObject jsonObject = (JSONObject) obj;
                String countryName = jsonObject.get("country").toString();
                Integer maxCost = Integer.parseInt(jsonObject.get("max_cost").toString());
                if (countryName == "" ) {
                    throw new WanComException("Missing input: countryName");
                } else if (!(maxCost > 0)) {
                    throw new WanComException("Missing input: cost");
                }

                JSONObject jsonTopology = JSONUtils.JSONObjectFromJSONFile(countryName);
                System.out.println(jsonTopology.toString());

                Graph graph = JSONUtils.graphFromJSONTopology(jsonTopology);
                Graph newGraph = NewGraph.addBestNewNode(graph, countryName, maxCost);
                jsonResponse = JSONUtils.JSONTopologyFromGraph(newGraph);
                System.out.println("newGraph " + jsonResponse);

            } catch (ParseException e) {
                System.err.println("Parsing error");
            } catch (WanComException e) {
                System.err.println(e.getMessage());
            }

            return jsonResponse;
        });
    }
}
