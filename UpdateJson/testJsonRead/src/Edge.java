public class Edge {
    //create a comparable interface
    private Vertex endPoint;
    private double weight;

    public Vertex getEndPoint() {
        return endPoint;
    }
    public void setEndPoint(Vertex endPoint) {
        this.endPoint = endPoint;
    }
    public double getWeight() {
        return weight;
    }
    public void setWeight(int weight) {
        this.weight = weight;
    }
    public Edge(Vertex endPoint, double weight) {
        //super();// super() is used to call immediate parent.
        this.endPoint = endPoint;
        this.weight = weight;
    }

}
