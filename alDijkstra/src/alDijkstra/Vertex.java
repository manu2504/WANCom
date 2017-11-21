package alDijkstra;

public class Vertex {
	
	private String id;
    private String name;
    double corLat;
    double corLong;
    
    public Vertex(String id, String name, double corLat, double corLong) {
        this.id = id;
        this.name = name;
        this.corLat=corLat;
        this.corLong=corLong;
    }
    
    public Vertex (double corLat, double corLong) {
    	this.corLat=corLat;
    	this.corLong=corLong;
    }
    
    public String getId() {
        return id;
    }
    
    public String getName() {
        return name;
    }
    
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((id == null) ? 0 : id.hashCode());
        return result;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Vertex other = (Vertex) obj;
        if (id == null) {
            if (other.id != null)
                return false;
        } else if (!id.equals(other.id))
            return false;
        return true;
    }
    @Override
    public String toString() {
        return "Vertex [ lat=" + corLat + ", Long="
                + corLong + "]";
    }
   

}
