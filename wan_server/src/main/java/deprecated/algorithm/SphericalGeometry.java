package deprecated.algorithm;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SphericalGeometry {

  // distance is in km
  public static int getDistance(double lat1, double lon1, double lat2, double lon2) {
    double theta = lon1 - lon2;
    double dist = Math.sin(degreeToRadiens(lat1)) * Math.sin(degreeToRadiens(lat2))
        + Math.cos(degreeToRadiens(lat1)) * Math.cos(degreeToRadiens(lat2)) * Math.cos(degreeToRadiens(theta));
    dist = Math.acos(dist);
    dist = radiensTodegrees(dist);
    dist = dist * 60 * 1.1515;
    dist = dist * 1.609344;
    return (int) dist;
  }

  private static double degreeToRadiens(double degree) {
    return (degree * Math.PI / 180.0);
  }

  private static double radiensTodegrees(double radines) {
    return (radines * 180 / Math.PI);
  }
  
  /*
   * This function computes the coordinates of the intersection
   * between a circle and a line on a sphere, and prints it.
   * Earth can be considered as a sphere with an error up to 0.3%[1].
   * This allows to determine a new hop located on an existing path
   * at the optimal position while respecting the constraint.
   * 
   * This Java code has been translated from the R code located in [1].
   * 
   * [1] https://gis.stackexchange.com/questions/36841/line-intersection-with-circle-on-a-sphere-globe-or-earth#answer-36979
   */
  public static void printIntersectionPoints() {
    double r; // radius (in meters)
    double alpha, beta, gamma;
    Map<String, Double> a0, b0, c0, A, B, C, u, v, t, h0;
    a0 = new HashMap<String, Double>();
    b0 = new HashMap<String, Double>();
    c0 = new HashMap<String, Double>();
    A = new HashMap<String, Double>();
    B = new HashMap<String, Double>();
    C = new HashMap<String, Double>();
    u = new HashMap<String, Double>();
    v = new HashMap<String, Double>();
    t = new HashMap<String, Double>();
    h0 = new HashMap<String, Double>();
    List<Double> x = new ArrayList<Double>();

    // Constants
    double degree = 2.0 * Math.PI / 360.0;
    double radian = 1.0 / degree;
    double radius = 6371007.2; // meters
        
    // Input
    a0.put("lat", 32.78306 * degree);  a0.put("lng", -96.80667 * degree); // Point A in (lat, lon) (in this example -> Dallas)
    b0.put("lat", 29.76328 * degree);  b0.put("lng", -95.36327 * degree); // Point B (in this example -> Houston)
    c0.put("lat", 29.95465 * degree);  c0.put("lng", -90.07507 * degree); // Center (in this example -> New Orleans)
    r = 650.0 * 1000.0; // constraint, in meters (radius of the circle)
    System.out.println("a0="+a0.toString() + ", b0="+b0.toString() + ", c0="+c0.toString());
    
    // Projection
    A.put("lat", a0.get("lat") * 1 * radius);  A.put("lng", a0.get("lng") * Math.cos(c0.get("lat")) * radius );
    B.put("lat", b0.get("lat") * 1 * radius);  B.put("lng", b0.get("lng") * Math.cos(c0.get("lat")) * radius );
    C.put("lat", c0.get("lat") * 1 * radius);  C.put("lng", c0.get("lng") * Math.cos(c0.get("lat")) * radius );
    System.out.println("A="+A.toString() + ", B=" + B.toString() + ", C=" + C.toString());
    
    // Compute coefficients of the quadratic equation
    v.put("lat", A.get("lat") - C.get("lat"));  v.put("lng", A.get("lng") - C.get("lng"));
    u.put("lat", B.get("lat") - A.get("lat"));  u.put("lng", B.get("lng") - A.get("lng"));
    alpha = u.get("lat") * u.get("lat") + u.get("lng") * u.get("lng");
    beta = u.get("lat") * v.get("lat") + u.get("lng") * v.get("lng");
    gamma = v.get("lat") * v.get("lat") + v.get("lng") * v.get("lng") - r*r;
    System.out.println("alpha="+alpha + ", beta=" + beta + ", gamma=" + gamma);
    
    // Solve the equation.
    t.put("lat", ( -beta + Math.sqrt(beta*beta - alpha * gamma) ) / alpha );
    t.put("lng", ( -beta - Math.sqrt(beta*beta - alpha * gamma) ) / alpha );
    System.out.println(t.toString());
    List<Double> tl = new ArrayList<Double>();
    if (t.get("lat") >= 0.0 && t.get("lat") <= 1.0) { // Limit the solution to arc a0-b0.
      tl.add(t.get("lat"));
    }
    if (t.get("lng") >= 0 && t.get("lng") <= 1) {
      tl.add(t.get("lng"));
    }
    
    if (tl.isEmpty()) {
      System.out.println("No intersection!");
      return;
    }
    
    // attempt:
    h0.put("lat", b0.get("lat") - a0.get("lat"));  h0.put("lng", b0.get("lng") - a0.get("lng")); // h0 = b0-a0 (cf. R code)
    
    if (tl.size() == 1) {
      System.out.println("tl size == 1");
      x.add(0, (a0.get("lat") + h0.get("lat") * tl.get(0)) * radian);
      x.add(1, (a0.get("lng") + h0.get("lng") * tl.get(0)) * radian);
      System.out.println(x.toString());
    } else if (tl.size() == 2) {
      System.out.println("tl size == 2");
      x.add(0, (a0.get("lat") + h0.get("lat") * tl.get(0)) * radian);  x.add(1, (a0.get("lng") + h0.get("lng") * tl.get(0)) * radian);
      x.add(2, (a0.get("lat") + h0.get("lat") * tl.get(1)) * radian);  x.add(3, (a0.get("lng") + h0.get("lng") * tl.get(1)) * radian);
      System.out.println(x.toString());
    } else {
      System.err.println("tl.size() == " + tl.size() + " !");
    }
  }
  
  /*
   * This function is very similar, unless it is not designed for testing,
   * but instead returns the coordinates of the point(s) of intersection
   * as a list of Coordinate objects (this list contains 0, 1 or 2 elements)
   */
  public static List<Coordinates> intersectionPoint(Coordinates coords_center, Coordinates coords_second_point,
      Coordinates coords_third_point, double max_distance) {
    
    List<Coordinates> res = new ArrayList<Coordinates>();
    
    double alpha, beta, gamma;
    Map<String, Double> A, B, C, u, v, t, h0;
    A = new HashMap<String, Double>();
    B = new HashMap<String, Double>();
    C = new HashMap<String, Double>();
    u = new HashMap<String, Double>();
    v = new HashMap<String, Double>();
    t = new HashMap<String, Double>();
    h0 = new HashMap<String, Double>();
    List<Double> x = new ArrayList<Double>();

    // Constants
    double degree = 2.0 * Math.PI / 360.0;
    double radian = 1.0 / degree;
    double radius = 6371007.2; // meters

    System.out.println("coords_center="+coords_center.toString() + ", coords_second_point="+coords_second_point.toString() + ","
        + "coords_third_point="+coords_third_point.toString());
    
    // Projection
    A.put("lat", coords_center.lat * 1 * radius);  A.put("lng", coords_center.lng * Math.cos(coords_third_point.lat) * radius );
    B.put("lat", coords_second_point.lat * 1 * radius);  B.put("lng", coords_second_point.lng * Math.cos(coords_third_point.lat) * radius );
    C.put("lat", coords_third_point.lat * 1 * radius);  C.put("lng", coords_third_point.lng * Math.cos(coords_third_point.lat) * radius );
    System.out.println("A="+A.toString() + ", B=" + B.toString() + ", C=" + C.toString());
    
    // Compute coefficients of the quadratic equation
    v.put("lat", A.get("lat") - C.get("lat"));  v.put("lng", A.get("lng") - C.get("lng"));
    u.put("lat", B.get("lat") - A.get("lat"));  u.put("lng", B.get("lng") - A.get("lng"));
    alpha = u.get("lat") * u.get("lat") + u.get("lng") * u.get("lng");
    beta = u.get("lat") * v.get("lat") + u.get("lng") * v.get("lng");
    gamma = v.get("lat") * v.get("lat") + v.get("lng") * v.get("lng") - max_distance*max_distance;
    System.out.println("alpha="+alpha + ", beta=" + beta + ", gamma=" + gamma);
    
    // Solve the equation.
    t.put("lat", ( -beta + Math.sqrt(beta*beta - alpha * gamma) ) / alpha );
    t.put("lng", ( -beta - Math.sqrt(beta*beta - alpha * gamma) ) / alpha );
    System.out.println(t.toString());
    List<Double> tl = new ArrayList<Double>();
    if (t.get("lat") >= 0.0 && t.get("lat") <= 1.0) { // Limit the solution to arc a0-b0.
      tl.add(t.get("lat"));
    }
    if (t.get("lng") >= 0 && t.get("lng") <= 1) {
      tl.add(t.get("lng"));
    }
    
    if (tl.isEmpty()) {
      System.out.println("No intersection!");
      return res;
    }
    
    // attempt:
    h0.put("lat", coords_second_point.lat - coords_center.lat);  h0.put("lng", coords_second_point.lng - coords_center.lng); // h0 = b0-a0 (cf. R code)
    
    if (tl.size() == 1) {
      System.out.println("tl size == 1");
      double lat, lng;
      lat = (coords_center.lat + h0.get("lat") * tl.get(0)) * radian;
      lng = (coords_center.lng + h0.get("lng") * tl.get(0)) * radian;
      x.add(0, lat);
      x.add(1, lng);
      System.out.println(x.toString());
      res.add(new Coordinates(lat, lng));
    } else if (tl.size() == 2) {
      System.out.println("tl size == 2");
      double lat1, lng1, lat2, lng2;
      lat1 = (coords_center.lat + h0.get("lat") * tl.get(0)) * radian;
      lng1 = (coords_center.lng + h0.get("lng") * tl.get(0)) * radian;
      lat2 = (coords_center.lat + h0.get("lat") * tl.get(1)) * radian;
      lng2 = (coords_center.lng + h0.get("lng") * tl.get(1)) * radian;
      x.add(0, lat1);  x.add(1, lng1);
      x.add(2, lat2);  x.add(3, lng2);
      System.out.println(x.toString());
      res.add(new Coordinates(lat1, lng1));
      res.add(new Coordinates(lat2, lng2));
    } else {
      System.err.println("tl.size() == " + tl.size() + " !");
    }
    
    return res;
  }
}
