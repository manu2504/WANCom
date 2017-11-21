package alDijkstra;

public class Coordinate {

	double srcLat;
	double srcLong;
	double dstLat;
	double dstLong;
	
	
	public Coordinate(double srcLat, double srcLong, double dstLat, double dstLong) {
		super();
		this.srcLat=srcLat;
		this.srcLong=srcLong;
		this.dstLat= dstLat;
		this.dstLong=dstLong;
	}


	public double getSrcLat() {
		return srcLat;
	}


	public void setSrcLat(double srcLat) {
		this.srcLat = srcLat;
	}


	public double getSrcLong() {
		return srcLong;
	}


	public void setSrcLong(double srcLong) {
		this.srcLong = srcLong;
	}


	public double getDstLat() {
		return dstLat;
	}


	public void setDstLat(double dstLat) {
		this.dstLat = dstLat;
	}


	public double getDstLong() {
		return dstLong;
	}


	public void setDstLong(double dstLong) {
		this.dstLong = dstLong;
	}
	
	
	 @Override
     public String toString() {
         return "Coordinates [ scrlat=" + srcLat + ", srcLong="
                 + srcLong + ", dstlat=" + dstLat + ", dstLong=" + dstLong + "]";
     }
	
}
