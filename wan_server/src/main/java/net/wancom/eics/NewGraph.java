package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

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
    Map<String, Node> mapNodes = new HashMap<>();//not necessary 
    for (int i=0; i<nodesList.size();i++){
      JSONObject nodeObject = (JSONObject) nodesList.get(i);
      Node node = new Node("this node"+i);
      double nodeLat = Double.parseDouble(nodeObject.get("Latitude").toString());
      double nodeLong= Double.parseDouble(nodeObject.get("Longitude").toString());
      node.setLatitude(nodeLat);
      node.setLongitude(nodeLong);
      mapNodes.put("this node" +i,node); //this might not be necessary
      graph.addNode(node); // this means that every nodes is in the graph

      //TODO: test each individual node with the preexisting nodes in the graph and calculate the distance between them
      //TODO:

    }

    // TODO
    
    return Graph.initGraph();
  }

}
