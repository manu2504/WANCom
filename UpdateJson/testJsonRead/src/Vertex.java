import java.util.ArrayList;
import java.util.Collections;

public class Vertex {
    private int num;
    private ArrayList<Edge> edges;
    private boolean isVisited;
    private Double distance;
    //before private int parent
    private String parent;
    private int node;
    private double corLat;
    private double corLong;
    private String id;

    public int getNode() {
        return node;
    }
    public void setNode(int node) {
        this.node = node;
    }
    public Vertex(double corLat, double corLong, String id ) {
        super();
        this.corLat = corLat;
        this.corLong=corLong;
        this.id=id;
        this.node=num;
        this.edges=new ArrayList<>();
        this.isVisited=false;
        this.distance=Double.MAX_VALUE;
// ，integer is a class, extension for int ,
//MAX_VALUE=2^32 -1

        //before  this.parent=-1;
        this.parent="";
    }
    public int getNum()
    {
        return num;
    }

    //added now
    public String getId(){
        return id;
    }

    public boolean isVisited()
    {
        return isVisited;
    }
    public void markVisited()
    {
        this.isVisited = true;
    }
    public Double getDistance() {
        return distance;
    }
    public void setDistance(Double distance) {
        this.distance = distance;
    }


    public void addEdge(Vertex vnum, double weight){
        edges.add(new Edge(vnum, weight));
        //Collections.sort(edges);
        // do not give a comparator ,  compare as default
    }

   // @Override
    /*
    public int compareTo(Vertex arg0) {
        return Integer.compare(distance, arg0.distance);
    }
    */
    public ArrayList<Edge> getEdges()
    {
        return edges;
    }

    public double getKey() {
        return distance;
    }

    @Override
    public String toString() {
        return "Vertex [num=" + num + ", distance=" + distance + ", parent="
                + parent + "]";
    }// override string to string


    //before :  public Integer getParent()
    public String getParent() {
        return parent;
    }
    //Before:  public void setParent(Integer parent)
    public void setParent(String parent) {
        this.parent = parent;
    }
}