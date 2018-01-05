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
        System.out.println("Server listening on port 4567 (type 'localhost:4567' in the address bar of your browser)");

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
                System.out.println("graph.getNodes()"+graph.getNodes().toString());
                System.out.println("graph.getNodes()"+graph.getNodes().toString());
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

                /*
                 *  TODO: since adding the best new node may take many hours (5-10) to run,
                 *  take the code from here and run it in standalone mode
                 *  and output the result to a text file
                 *  
                 *  Biwen's suggestion: We can use concurrent computing to make the code faster,
                 *  using a thread of pools, each pool trying to add one new node to the graph
                 *  (with all different combinations of links) and writing the result to a file
                 */
                JSONObject jsonTopology = JSONUtils.JSONObjectFromJSONFile(countryName);
                System.out.println(jsonTopology.toString());

                Graph graph = JSONUtils.graphFromJSONTopology(jsonTopology);
                Graph newGraph = NewGraph.addBestNewNode(graph, countryName, maxCost);
                if (newGraph == null) {
                    jsonResponse = new JSONObject();
                    jsonResponse.put("no_change", true);
                    return jsonResponse;
                }
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
