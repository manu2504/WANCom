package net.wancom.wan_server;

// We use the framework Spark for the webserver. See sparkjava.com/documentation.html
import static spark.Spark.*;

import net.wancom.eics.BetterGraph;
import net.wancom.eics.Distance;

//import net.wancom.eics.NewGraph;
import org.json.simple.JSONObject;
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
            String res = "";
            response.type("application/json");

            try {
                Object obj = parser.parse(request.body());
                JSONObject jsonObject = (JSONObject) obj;
                /*String countryName = jsonObject.get("country").toString();

                JSONObject jsonTopology = JSONUtils.JSONObjectFromJSONFile(countryName); */
                JSONObject jsonTopology = (JSONObject) jsonObject.get("topo");
                Graph graph = JSONUtils.graphFromJSONTopology(jsonTopology);
                String sourceNodeName = jsonObject.get("src").toString();
                String targetNodeName = jsonObject.get("dst").toString();
                Node sourceNode = graph.findNode(sourceNodeName);
                Node targetNode = graph.findNode(targetNodeName);
                if (sourceNode == null) {
                    res = "{\"error\": \"The source selected does not belong to the topology\"}";
                }
                if (targetNode == null) {
                    res = "{\"error\": \"The destination selected does not belong to the topology\"}";
                }
                
                Dijkstra.calculateShortestPathFromSource(graph, sourceNode);
                res = targetNode.getShortestPathWithTotalDistanceAsJSONString();
                System.out.println(res);
            } catch (ParseException e) {
                System.err.println("Parsing error");
            } catch (WanComException e) {
                System.err.println(e.getMessage());
            }

            return res;
        });

        post("/newgraph", (request, response) -> {
            System.out.println("data received: " + request.body());

            JSONParser parser = new JSONParser();
            JSONObject jsonResponse = null;

            try {
                Object obj = parser.parse(request.body());
                JSONObject jsonObject = (JSONObject) obj;
                String countryName = jsonObject.get("country").toString();
                String sourceNodeName = jsonObject.get("src").toString();
                String targetNodeName = jsonObject.get("dst").toString();
                Integer maxCost = Integer.parseInt(jsonObject.get("max_cost").toString());
                String accuracy = "high";
                if (countryName == "" ) {
                    throw new WanComException("Missing input: countryName");
                } else if (!(maxCost > 0)) {
                    throw new WanComException("Missing or incorrect input: cost: " + maxCost);
                }

                JSONObject jsonTopology = JSONUtils.JSONTopology(countryName);
                System.out.println(jsonTopology.toString());

                Graph graph = JSONUtils.graphFromJSONTopology(jsonTopology);
                //Graph newGraph = NewGraph.addBestNewNode(graph, countryName, maxCost);
                Graph newGraph = BetterGraph.addBestNewNode(graph, countryName, sourceNodeName, targetNodeName, maxCost, accuracy);
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
