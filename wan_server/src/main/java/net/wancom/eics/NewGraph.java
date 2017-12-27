package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import net.wancom.graph.*;
import net.wancom.json.JSONUtils;

public class NewGraph {
  
  /*
   * TODO: finish to write the function addBestNewNode(). This function requires:
   * (TODO) a function which evaluates the current total latency of a graph
   * (TODO) a function that adds a new node in a graph ( needs to use Graph.addNode() )
   * and after, a loop that iterates for all potential new nodes, and compute for each of them
   * the new total distance for the modified graph. This performance should be stored in a variable
   * that stores the best performance, and be replaced every time a better performance is found.
   */
  
  public Graph addBestNewNode(Graph graph, String country, int constraint) throws FileNotFoundException, IOException {
    JSONObject jsonObject = JSONUtils.JSONObjectFromJSONFile(country);
    JSONArray nodesList = (JSONArray) jsonObject.get("nodes");
    
    // TODO
    
    return Graph.initGraph();
  }

}
