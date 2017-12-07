package alDijkstra;


import java.util.List;

public class Graph {
	
	 private final List<Vertex> nodes;
	    private final List<Edge> edges;
	    
	    public Graph(List<Vertex> nodes, List<Edge> edges) {
	        this.nodes = nodes;
	        this.edges = edges;
	    }
	    
	   
	    public List<Vertex> getNodes() {
			return nodes;
		}


		public List<Edge> getEdges() {
	        return edges;
	    }

}
