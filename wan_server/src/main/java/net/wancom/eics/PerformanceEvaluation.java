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
	     // list of cost in Germany 
	     int size1 =3;
	     int[] cost_ger = new int[size1];
	     cost_ger[0] = 100;
	     cost_ger[1] = 350;
	     cost_ger[2] = 1000;
	     // list of cost in Finland//
	     int size2 =3;
	     int[] cost_fin = new int[size2];
	     cost_fin[0] = 110;
	     cost_fin[1] = 250;
	     cost_fin[2] = 700;
	    
	  // Create a stream to hold the output
	     ByteArrayOutputStream baos = new ByteArrayOutputStream();
	     PrintStream ps = new PrintStream(baos);
	     // IMPORTANT: Save the old System.out!
	     PrintStream old = System.out;
	     
	     //loop for Germany
	     org.json.simple.JSONObject jsonTopology = JSONUtils.JSONTopology("Germany");
	    
	  
	     for (int i=0;i<size;i++){
	    	 System.out.println("density=" + density[i]);
	    	 for (int c1=0;c1<size1;c1++){
	    		 System.out.println("cost=" + cost_fin[c1]);
	    		   for(int x=0;x<10;x++){

	    		 // Tell Java to use your special stream
	    		 System.setOut(ps);
	    		 
	    		 long start = System.currentTimeMillis();
		    	 Graph graphGermany = JSONUtils.graphFromJSONTopology(jsonTopology);
	 	    	 BetterGraph.addBestNewNode(graphGermany, "Germany", "GOE", "ILM",cost_ger[c1], density[i]);
	 	    	 long end = System.currentTimeMillis();
	 	    	 long totalTime = end - start;

	 	    	 // Put things back
	 	    	 System.out.flush();
	 	    	 System.setOut(old);
	 	        
	    		 System.out.println("Germany run for "+ x +" times ("+ totalTime + "ms)");
	 	    	
	    		 
	    	 }


          
	     }
	    	 System.out.println();
	     }
	     // loop for Finland
	     org.json.simple.JSONObject jsonTopology2 = JSONUtils.JSONTopology("Finland");
	     
	     for(int i=0;i<size;i++){
	    	 System.out.println("density=" + density[i]);
	    	 for(int c2=0;c2<size2;c2++){
	    		 System.out.println("cost=" + cost_fin[c2]);
	    		 for(int y=0;y<10;y++){ // test for 10 times

	    		 // Tell Java to use your special stream
	    		 System.setOut(ps);
	    		 
	    		 long start = System.currentTimeMillis();
	    		 Graph graphFinland = JSONUtils.graphFromJSONTopology(jsonTopology2);
	    		 BetterGraph.addBestNewNode(graphFinland, "Finland", "Pori", "Mikkeli",cost_fin[c2],  density[i]);
	    		 long end = System.currentTimeMillis();
	    		 long totalTime = end - start;

	 	    	 // Put things back
	 	    	 System.out.flush();
	 	    	 System.setOut(old);
	    		 System.out.println("Finland run for "+ y +" times ("+ totalTime + "ms)");
	    		
	    		 
	    		 
	    		 }
	    		 
	    	 }
	    	 System.out.println();
	     }
	  
	}
	

}