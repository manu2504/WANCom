package dijkstra;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

public class TestDijkstraAlgorithm {
    
    private static List<Vertex> nodes;
    private static List<Edge> edges;
    //private static List<Distance> duration;
    
    
    
    //public void testExcute() {
    public static void main(String[] args){
        nodes = new ArrayList<Vertex>();
        edges = new ArrayList<Edge>();
        // duration = new ArrayList<Duration>();
        
        for (int i = 0; i < 11; i++) {
            Vertex location = new Vertex("hop" + i, "hop"
                                         + "~" + i);
            nodes.add(location);
            ///edges.add(weight);
        }
        
        addLane("Edge_0", 0, 1, 85);
        addLane("Edge_1", 0, 2, 217);
        addLane("Edge_2", 0, 4, 173);
        addLane("Edge_3", 2, 6, 186);
        addLane("Edge_4", 2, 7, 103);
        addLane("Edge_5", 3, 7, 183);
        addLane("Edge_6", 5, 8, 250);
        addLane("Edge_7", 8, 9, 84);
        addLane("Edge_8", 7, 9, 167);
        addLane("Edge_9", 4, 9, 502);
        addLane("Edge_10", 9, 10, 40);
        addLane("Edge_11", 1, 10, 600);
        //reverse path
        addLane("Edge_0", 1, 0, 85);
        addLane("Edge_1", 2, 0, 217);
        addLane("Edge_2", 4, 0, 173);
        addLane("Edge_3", 6, 2, 186);
        addLane("Edge_4", 7, 2, 103);
        addLane("Edge_5", 7, 3, 183);
        addLane("Edge_6", 8, 5, 250);
        addLane("Edge_7", 9, 8, 84);
        addLane("Edge_8", 9, 7, 167);
        addLane("Edge_9", 9, 4, 502);
        addLane("Edge_10", 10, 9, 40);
        addLane("Edge_11", 10, 1, 600);
        //Array2CSV(alldata,"test.csv");
        
        
        
        // Lets check from location Loc_1 to Loc_10
        Graph graph = new Graph(nodes, edges);
        DijkstraAlgorithm dijkstra = new DijkstraAlgorithm(graph);
        Scanner reader = new Scanner(System.in);  // Reading from System.in
        System.out.println("Enter a source hop: ");
        int n = reader.nextInt(); // Scans the next token of the input as an int.
        System.out.println("Enter a dst hop: ");
        int m = reader.nextInt();
        //once finished
        
        
        reader.close();
        long start=System.currentTimeMillis();   //获取开始时间
        dijkstra.execute(nodes.get(n));
        LinkedList<Vertex> path = dijkstra.getPath(nodes.get(m));
        
        
        // assertNotNull(path);
        // assertTrue(path.size() > 0);
        System.out.println( "the shortest path from " + n +" to "+ m );
        long end = System.currentTimeMillis();
        System.out.println("Time to find shortest path (first time) from " + n + " to " + m + ": " + (end-start) + "ms");
        for (Vertex vertex : path) {
            System.out.println(vertex);
        }
        
        // for (Vertex vertex : path) {
        //  double sumDistance =0;
        
        
        
        //System.out.println( vertex.weight);
        //}
        
    }
    
    private static void addLane(String laneId, int sourceLocNo, int destLocNo, int duration) {
        Edge lane = new Edge(laneId, nodes.get(sourceLocNo), nodes.get(destLocNo), duration);
        edges.add(lane);
    }
    
    // private static class Distance {
    
    // public Distance() {
    
    //}
    //}
    
    
    
    
}


