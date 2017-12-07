package alDijkstra;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;



public class TestDijkstraAlgorithm {
	
	private static List<Vertex> nodes;
	private static List<Edge> edges;
	//Arraylist that contains coordinates fetched from txt file.
	private static ArrayList<Coordinate> coordinates;
	//Arrraylist to store distances between two points.
	private static ArrayList<Double> dist;

	public static void main(String[] args) throws NumberFormatException, IOException{
		nodes = new ArrayList<Vertex>();
		edges = new ArrayList<Edge>();
		coordinates = new ArrayList<Coordinate>();
		dist = new ArrayList<Double>();
		
		try {
			BufferedReader inSrc = new BufferedReader(new FileReader("C:\\Users\\ibrah\\Desktop\\coordinates.txt"));
			String str;	
			int i = 0;
			//Read the txt file that contains coordinates line by line 
			while((str =inSrc.readLine()) != null) {
				String[] ar = str.split(",");	
				coordinates.add(new Coordinate(Double.parseDouble(ar[0]),Double.parseDouble(ar[1]),Double.parseDouble(ar[2]),Double.parseDouble(ar[3])));
				nodes.add(new Vertex(Double.parseDouble(ar[0]),Double.parseDouble(ar[1])));
				nodes.add(new Vertex(Double.parseDouble(ar[2]),Double.parseDouble(ar[3])));
			}
			
			for (Coordinate cord : coordinates) {
				double distance=getDistance(cord.srcLat, cord.getSrcLong(), cord.getDstLat(),cord.getDstLong());
				dist.add(distance); 	
				addLane("Edge_"+ i, cord.srcLat,cord.srcLong, cord.dstLat, cord.dstLong,distance);
				i++;
			}
			inSrc.close();
			System.out.println("here:" +dist);
			System.out.println(coordinates);
			

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		// Lets check from location Loc_1 to Loc_10
		Graph graph = new Graph(nodes, edges);
		DijkstraAlgorithm dijkstra = new DijkstraAlgorithm(graph);
		
		
		int n=0;
		int m=1;
		nodes.forEach(node -> System.out.println(node));
		edges.forEach(node-> System.out.println(node));
		dijkstra.execute(nodes.get(n));
		LinkedList<Vertex> path = dijkstra.getPath(nodes.get(m));


		System.out.println( "the shortest path from " + nodes.get(n) +" to "+ nodes.get(m) );
	/*	
		long end = System.currentTimeMillis();
		System.out.println("Time to find shortest path (first time) from " + n + " to " + m + ": " + (end-start) + "ms");
		for (Vertex vertex : path) {
			System.out.print(" "+vertex);
		}
*/

	}

	private static double getDistance(double lat1, double lon1, double lat2, double lon2) {
		double theta = lon1 - lon2;
		double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2)) + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos( degreeToRadiens(theta));
		dist = Math.acos(dist);
		dist =radiensTodegrees(dist);
		dist = dist * 60 * 1.1515;
		dist = dist * 1.609344;
		return (dist);
	}

	private static double degreeToRadiens(double degree) {
		return (degree * Math.PI / 180.0);
	}

	private static double radiensTodegrees(double radines) {
		return (radines * 180 / Math.PI);
	}

	private static void addLane(String laneId,double srclat, double srclong, double dstlat, double dstlong, double duration) {
		Edge lane = new Edge(laneId, new Vertex(srclat, srclong), new Vertex(dstlat,dstlong), duration);
		edges.add(lane);
	}






}
