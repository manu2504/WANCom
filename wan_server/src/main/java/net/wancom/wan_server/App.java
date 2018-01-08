package net.wancom.wan_server;

// We use the framework Spark for the webserver. See sparkjava.com/documentation.html
import static spark.Spark.*;

import net.wancom.eics.NewGraph;
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
                    response.type("application/json");
                    res = "{\"error\": \"The source selected does not belong to the topology\"}";
                }
                if (targetNode == null) {
                    response.type("application/json");
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
