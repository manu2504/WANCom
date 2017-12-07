
/
package model;

import java.util.ArrayList;
import java.util.Collections;

public class Vertex implements Comparable<Vertex>{ 
    //create a comparable interface

	private int num;
	private ArrayList<Edge> edges;
	private boolean isVisited;
	private Integer distance;
	private int parent;
	private int node;
	public int getNode() {
		return node;
	}
	public void setNode(int node) {
		this.node = node;
	}
	public Vertex(int num) {
		super();
		this.num = num;
		this.node=num;
		this.edges=new ArrayList<>();
		this.isVisited=false;
		this.distance=Integer.MAX_VALUE;
// ，integer is a class, extension for int ,
//MAX_VALUE=2^32 -1
		this.parent=-1;
	}
	public int getNum() {
		return num;
	}
	public boolean isVisited() {
		return isVisited;
	}
	public void markVisited() {
		this.isVisited = true;
	}
	public Integer getDistance() {
		return distance;
	}
	public void setDistance(Integer distance) {
		this.distance = distance;
	}
	public void addEdge(Integer vnum, int weight){
		edges.add(new Edge(vnum, weight));
		Collections.sort(edges);
        // do not give a comparator ,  compare as default
	}
	@Override
	public int compareTo(Vertex arg0) {
		return Integer.compare(distance, arg0.distance);
	}	
	public ArrayList<Edge> getEdges(){
		return edges;
	}
	public Integer getKey() {		
		return distance;
	}
	@Override
	public String toString() {
		return "Vertex [num=" + num + ", distance=" + distance + ", parent="
				+ parent + "]";
	}// override string to string 
	public int getParent() {
		return parent;
	}
	public void setParent(int parent) {
		this.parent = parent;
	}	
}
