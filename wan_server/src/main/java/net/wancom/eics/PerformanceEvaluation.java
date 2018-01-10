package net.wancom.eics;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;

import net.sf.json.JSONObject;
import net.wancom.graph.Graph;
import net.wancom.json.JSONUtil;
import net.wancom.json.JSONUtils;

public class PerformanceEvaluation {

	public static void main(String[] args) throws FileNotFoundException, IOException {
		// TODO Auto-generated method stub
		int size = 3;
		//list of density
	      String[] density = new String[size];
	     density[0] = "low";
	     density[1] = "middle";
	     density[2] = "high";
	     // list of cost in usa 
	     int size1 =3;
	     int[] cost_ger = new int[size1];
	     cost_ger[0] = 120;
	     cost_ger[1] = 300;
	     cost_ger[2] = 1000;
	     // list of cost in China//
	     int size2 =3;
	     int[] cost_fin = new int[size2];
	     cost_fin[0] = 200;
	     cost_fin[1] = 650;
	     cost_fin[2] = 1400;
	    
	  // Create a stream to hold the output
	     ByteArrayOutputStream baos = new ByteArrayOutputStream();
	     PrintStream ps = new PrintStream(baos);
	     // IMPORTANT: Save the old System.out!
	     PrintStream old = System.out;
	     
	     //loop for Germany
	     org.json.simple.JSONObject jsonTopology = JSONUtils.JSONTopology("USA");
	    
	  
	     for (int i=0;i<size;i++){
	    	 System.out.println("density=" + density[i]);
	    	 for (int c1=0;c1<size1;c1++){
	    		 System.out.println("cost=" + cost_ger[c1]);
	    		   for(int x=0;x<10;x++){

	    		 // Tell Java to use your special stream
	    		 System.setOut(ps);
	    		 
	    		 long start = System.currentTimeMillis();
		    	 Graph graphUSA = JSONUtils.graphFromJSONTopology(jsonTopology);
	 	    	 BetterGraph.addBestNewNode(graphUSA, "USA", "Edmonton", "Miami",cost_ger[c1], density[i]);
	 	    	 long end = System.currentTimeMillis();
	 	    	 long totalTime = end - start;

	 	    	 // Put things back
	 	    	 System.out.flush();
	 	    	 System.setOut(old);
	 	        
	    		 System.out.println("USA runs for "+ x +" times ("+ totalTime + "ms)");
	 	    	
	    		 
	    	 }


          
	     }
	    	 System.out.println();
	     }
	     // loop for Finland
	     org.json.simple.JSONObject jsonTopology2 = JSONUtils.JSONTopology("China");
	     
	     for(int i=0;i<size;i++){
	    	 System.out.println("density=" + density[i]);
	    	 for(int c2=0;c2<size2;c2++){
	    		 System.out.println("cost=" + cost_fin[c2]);
	    		 for(int y=0;y<10;y++){ // test for 10 times

	    		 // Tell Java to use your special stream
	    		 System.setOut(ps);
	    		 
	    		 long start = System.currentTimeMillis();
	    		 Graph graphChina = JSONUtils.graphFromJSONTopology(jsonTopology2);
	    		 BetterGraph.addBestNewNode(graphChina, "China", "Kashi", "Guangzhou",cost_fin[c2],  density[i]);
	    		 long end = System.currentTimeMillis();
	    		 long totalTime = end - start;

	 	    	 // Put things back
	 	    	 System.out.flush();
	 	    	 System.setOut(old);
	    		 System.out.println("China runs for "+ y +" times ("+ totalTime + "ms)");
	    		
	    		 
	    		 
	    		 }
	    		 
	    	 }
	    	 System.out.println();
	     }
	  
	}
	

}
