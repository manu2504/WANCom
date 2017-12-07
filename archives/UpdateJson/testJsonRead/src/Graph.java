import java.util.ArrayList;
import java.util.Map;

public class Graph {
    private Map<String,Vertex> graph;

    /*maybe this is not needed */
    public Graph(Map<String,Vertex> vertices) {
        this.graph = vertices;

    }

// change this so that it takes (double srclat, double srclong , double dstLat, double dstLong, double distance)
    public void addUnorientedEdge(String src, String dst, double weight){
        //this .graph[srclat, srclong].addEdge(dstLat, dstLong, distance);
        graph.get(src).addEdge(graph.get(dst), weight);
        //this .graph[dstLat, dstLong].addEdge(srclat, srclong, distance);
        graph.get(dst).addEdge(graph.get(src),weight);

    }

     public void addOrientedEdge(String src, String dst, double weight){
          graph.get(src).addEdge(graph.get(dst),weight);
     }

    public Vertex getVertex(String id)
    {
        return graph.get(id);
    }

    public Map<String, Vertex> getAll()
    {
        return graph;
    }
}
