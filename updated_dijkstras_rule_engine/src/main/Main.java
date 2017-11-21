
package main;

import java.io.FileNotFoundException;
import java.util.LinkedList;

import model.Graph;
import dijkstra.Dijkstra;
import java.util.Scanner;
import reading.ReadGraph;

public class Main {

	public static void main(String[] args) throws FileNotFoundException {
		Graph g= ReadGraph.ReadUnorientedGraphFromEdgeList("/Users/biwen/Desktop/EdgeListTest");
                 //Scanner reader = new Scanner(System.in);  // Reading from System.in
                  //System.out.println("Enter a source hop: ");
                  // Integer x = reader.nextInt();
                  // System.out.println("Enter a dst hop: ");
                   // Integer y = reader.nextInt();
                    // Scanner in = new Scanner(System.in); 
    
                    
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
 