package net.wancom.eics;

import java.io.FileNotFoundException;
import java.io.IOException;

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
	     //loop for Germany
	     org.json.simple.JSONObject jsonTopology = JSONUtils.JSONTopologyFromJSONFile("Germany");
	    
	     for(int x=0;x<10;x++){
	     for (int i=0;i<size;i++){
	    	 for (int c1=0;c1<size1;c1++){
	    		 long start = System.currentTimeMillis();
		    	 Graph graphGermany = JSONUtils.graphFromJSONTopology(jsonTopology);
	 	    	 BetterGraph.addBestNewNode(graphGermany, "Germany", "GOE", "ILM",cost_ger[c1], density[i]);
	 	    	 long end = System.currentTimeMillis();
	 	    	 long totalTime = start - end;
	 	    	 System.out.printf("Germany run for"+ x+"times"+totalTime);
	 	    	 
	    		 
	    	 }


          
	     }
	     }
	     // loop for Finland
	     org.json.simple.JSONObject jsonTopology2 = JSONUtils.JSONTopologyFromJSONFile("Finland");
	     for(int y=0;y<10;y++){ // test for 10 times
	     for(int i=0;i<size;i++){
	    	 for(int c2=0;c2<size2;c2++){
	    		 long start = System.currentTimeMillis();
	    		 Graph graphFinland = JSONUtils.graphFromJSONTopology(jsonTopology2);
	    		 BetterGraph.addBestNewNode(graphFinland, "Finland", "Pori", "Mikkeli",cost_fin[c2],  density[i]);
	    		 long end = System.currentTimeMillis();
	    		 long totalTime = start - end;
	    		 System.out.printf("Finland run for"+ y+"times"+ totalTime );
	    		
	    		 
	    		 
	    	 }
	    	 
	     }
	     }
	  
	}
	

}
