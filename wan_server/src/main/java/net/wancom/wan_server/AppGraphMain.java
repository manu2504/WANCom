package net.wancom.wan_server;

import net.wancom.exceptions.WanComException;
import net.wancom.graph.Graph;
import net.wancom.graph.Node;
import net.wancom.json.JSONCountry;
import net.wancom.json.JSONLink;
import net.wancom.json.JSONNode;
import net.wancom.json.JSONUtil;

import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class AppGraphMain {
    public static void main(String[] args) {
        //TODO How to get each country as json ... you should solve it here
        //We pretend that we get country name from somewhere and name it country. I use Scanner to test.
        Scanner keyboard = new Scanner(System.in);
        System.out.println("Let me know the country that you will trace a graph: ");
        String strCountry = keyboard.nextLine();
        try {
            JSONCountry country = JSONUtil.unmarshalJsonCountry(strCountry);
            Graph graph = createTheGraph(country);
            //run the dijkstra ...
        } catch (WanComException we) {
            System.out.println("There is a problem (finding the file or parsing the json) and graph cannot be created: " + we.getMessage());
            we.printStackTrace();
        } catch (Exception e) {
            System.out.println("Something went wrong: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * TODO method is not completed yet
     * The following method take json nodes and link and create all nodes of type(@see{{@link Node}}.
     * The initiated nodes has all neighbors as a list parameter in it.
     * The graph will be created and ready to run dijkstra algorithm.
     * @param country the name of country you are going to create graph
     * @return the created graph ready to run dijkstra
     */
    public static Graph createTheGraph(JSONCountry country) {
        Graph graph = Graph.initGraph();
        List<JSONNode> jsonNodes = country.getNodes();
        List<JSONLink> jsonLinks = country.getLinks();
        Iterator<JSONNode> jsonNodeIterator = jsonNodes.iterator();
        Iterator<JSONLink> jsonLinkIterator = jsonLinks.iterator();
        if(jsonNodeIterator == null ){
            throw new WanComException("The system cannot fetch any node from json file. Please control " + country + ".json first and run the application again.");
        }
        if(jsonLinkIterator == null ){
            throw new WanComException("The system cannot fetch any link from json file. Please control " + country + ".json first and run the application again.");
        }
        
        //Uncomplete method. Should complete it.
        while (jsonNodeIterator.hasNext()){
            JSONNode jsonNode = jsonNodeIterator.next();
            String jsonNodeId = jsonNode.getId();
            Node node = new Node(jsonNodeId);
            jsonLinkIterator = jsonLinks.iterator();
            //We have to find all nearest adjacency of above node via link list we have.
            while (jsonLinkIterator.hasNext()){
                JSONLink jsonLink = jsonLinkIterator.next();
                String source = jsonLink.getSource();
                //source in jsonLink is the same as jsonNode id.
                if (source!=null && source.trim().equalsIgnoreCase(jsonNodeId.trim())){
                    
                }
            }
        }

        return graph;
    }
}
