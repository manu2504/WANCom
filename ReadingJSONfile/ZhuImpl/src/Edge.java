public class Edge implements Comparable<Edge>{
    //create a comparable interface
    private Integer endPoint;
    private Integer weight;

    public Integer getEndPoint() {
        return endPoint;
    }
    public void setEndPoint(Integer endPoint) {
        this.endPoint = endPoint;
    }
    public int getWeight() {
        return weight;
    }
    public void setWeight(int weight) {
        this.weight = weight;
    }
    public Edge(Integer endPoint, int weight) {
        //super();// super() is used to call immediate parent.
        this.endPoint = endPoint;
        this.weight = weight;
    }
    @Override
    public int compareTo(Edge arg0) {
        return this.weight.compareTo(arg0.weight);
    }
}
