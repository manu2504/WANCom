import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.NavigableSet;
import java.util.TreeSet;

public class Graph {
    private final Map<String, Vertex> graph; // mapping of vertex names to Vertex objects, built from a set of Edges
    /** One edge of the graph (only used by Graph constructor) */
    public static class Edge {
        public final String source, destination;
        public final int distance;

        public Edge(String source, String destination, int distance) {
            this.source = source;
            this.destination = destination;
            this.distance = distance;
        }

    }
    /** One vertex of the graph, complete with mappings to neighbouring vertices */
    public static class Vertex implements Comparable<Vertex> {
        public final String name;
        public int distance = Integer.MAX_VALUE; // MAX_VALUE assumed to be infinity
        public Vertex previous = null;
        public final Map<Vertex, Integer> neighbours = new HashMap<Vertex, Integer>();

        public Vertex(String name) {
            this.name = name;
        }

        private void printPath() {
            JSONArray jsonArray = new JSONArray();
            JSONObject jsonObj = new JSONObject();
            if (this == this.previous) {
               // jsonObj.put("source", this.name);

                 System.out.printf("%s", this.name);

            } else if (this.previous == null) {
                System.out.printf("%s(unreached)", this.name);
            }

            else {
                this.previous.printPath();
                //jsonObj.put("target", this.name);
                   System.out.printf(" -> %s(%d)", this.name, this.distance);
            }
            //jsonArray.add(jsonObj);

           // try {

                // Writing to a file
                //File file=new File("C:\\Users\\ibrah\\Desktop\\Utest.json");
                // file.createNewFile();
                //FileWriter fileWriter = new FileWriter(file);
                // System.out.println("Writing JSON object to file");
                //   System.out.println("-----------------------");
               // System.out.print(jsonArray);
              //  fileWriter.write(jsonArray.toJSONString());
               // fileWriter.flush();
                //fileWriter.close();

            //} catch (IOException e) {
              //  e.printStackTrace();
            //}
        }

        public int compareTo(Vertex other) {
            if (distance ==other.distance)
                return name.compareTo(other.name);
            return Integer.compare(distance, other.distance);
        }
    }
    /** Builds a graph from a set of edges */
    public Graph(Edge[] edges) {
        graph = new HashMap<String, Vertex>(edges.length);

        //one pass to find all vertices
        for (Edge e : edges) {
            if (!graph.containsKey(e.source))
                graph.put(e.source, new Vertex(e.source));
            if (!graph.containsKey(e.destination))
                graph.put(e.destination, new Vertex(e.destination));
        }

        //another pass to set neighbouring vertices
        for (Edge e : edges) {
            graph.get(e.source).neighbours.put(graph.get(e.destination), e.distance);
            graph.get(e.destination).neighbours.put(graph.get(e.source), e.distance); // also do this for an undirected graph
        }
    }
    /** Runs dijkstra using a specified source vertex */
    public void dijkstra(String startName) {
        if (!graph.containsKey(startName)) {
            System.err.printf("Graph doesn't contain start vertex \"%s\"\n", startName);
            return;
        }
        final Vertex source = graph.get(startName);
        NavigableSet<Vertex> q = new TreeSet<Vertex>();

        // set-up vertices
        for (Vertex v : graph.values()) {
            v.previous = v == source ? source : null;
            v.distance = v == source ? 0 : Integer.MAX_VALUE;
            q.add(v);
        }

        dijkstra(q);
    }

    /** Implementation of dijkstra's algorithm using a binary heap. */
    private void dijkstra(final NavigableSet<Vertex> q) {
        Vertex u, v;
        while (!q.isEmpty()) {

            u = q.pollFirst(); // vertex with shortest distance (first iteration will return source)
            if (u.distance == Integer.MAX_VALUE)
                break; // we can ignore u (and any other remaining vertices) since they are unreachable

            //look at distances to each neighbour
            for (Map.Entry<Vertex, Integer> a : u.neighbours.entrySet()) {
                v = a.getKey(); //the neighbour in this iteration

                final int alternateDist = u.distance + a.getValue();
                if (alternateDist < v.distance) { // shorter path to neighbour found
                    q.remove(v);
                    v.distance = alternateDist;
                    v.previous = u;
                    q.add(v);
                }
            }
        }
    }

    /** Prints a path from the source to the specified vertex */
    public void printPath(String endName) {
        if (!graph.containsKey(endName)) {
            System.err.printf("Graph doesn't contain end vertex \"%s\"\n", endName);
            return;
        }

        graph.get(endName).printPath();
        System.out.println();
    }

    /** Prints the path from the source to every vertex (output order is not guaranteed) */
    public void printAllPaths() {
        for (Vertex v : graph.values()) {
            v.printPath();
            System.out.println();
        }
    }
}