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
            Graph graph = App.createTheGraph(country);
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

  }
