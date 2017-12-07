import jdk.nashorn.internal.parser.JSONParser;

import java.io.*;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;


public class Main {

    public static void main(String[] args) throws IOException {

        // here i need to add my code to read from json file get the content from it and then pass it to graph.

        //ReadUnorientedGraphFromEdgeList need to take more parameters


        Graph g = ReadGraph.ReadUnorientedGraphFromEdgeList("C:\\Users\\ibrah\\Desktop\\EdgeTest.txt");
        long start=System.currentTimeMillis();

        LinkedList<Integer> res=Dijkstra.doDijkstra(g, 1, 7);
        long end = System.currentTimeMillis();


        if(res!=null){
            System.out.println("length="+res.pollLast());
            System.out.println("path");
            for(Integer i:res)
                System.out.println(i);
            System.out.println("Time to find shortest path (first time) ：" + (end-start) + "ms");

        }

    }

}