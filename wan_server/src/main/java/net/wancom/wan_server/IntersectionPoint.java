package net.wancom.wan_server;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class IntersectionPoint {
  /*
   */

  /*
   * This function seeks to find the point of intersection between a circle on the Earth,
   * and a (curved) line defined by two points on the Earth. Earth is considered as a sphere
   * Error (due to considering the Earth as a sphere) is up to 0.3%
   * 
   * It computes and prints the coordinates of the point of intersection.
   * 
   * This Java code has been translated from the R code located here:
   * https://gis.stackexchange.com/questions/36841/line-intersection-with-circle-on-a-sphere-globe-or-earth#answer-36979
   */
  public static void test() {
    double r; // radius (in km)
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
    /*
    a0.put("lat", 48.139115 * degree);  a0.put("lng", 11.578081 * degree); // Point A in (lat, lon)
    b0.put("lat", 48.146303 * degree);  b0.put("lng", 11.593102 * degree); // Point B
    c0.put("lat", 48.137024 * degree);  c0.put("lng", 11.575249 * degree); // Center
    r = 1000.0; 
    */
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
    
    // TODO: translate this R statement to Java:
    // x <- (a0 + (b0-a0) %o% t) * radian  // Columns are (lat, lon)
    
    // attempt:
    h0.put("lat", b0.get("lat") - a0.get("lat"));  h0.put("lng", b0.get("lng") - a0.get("lng")); // h0 = b0-a0 (cf. R code)
    //y.put("lat", transposeMatrix(tl)); // TODO: transposeMatrix needs to return Array (not [][] like currently)
    
    if (tl.size() == 1) {
      System.out.println("tl size == 1");
      x.add(0, (a0.get("lat") + h0.get("lat") * tl.get(0)) * radian);
      x.add(1, (a0.get("lng") + h0.get("lng") * tl.get(0)) * radian);
      System.out.println(x.toString());
    } else if (tl.size() == 2) {
      System.out.println("tl size == 2");
//      x.add( h0.get("lat") * tl.get(0) );  x.add( h0.get("lng") * tl.get(0) );
//      x.add( h0.get("lat") * tl.get(1) );  x.add( h0.get("lng") * tl.get(1) );
      x.add(0, (a0.get("lat") + h0.get("lat") * tl.get(0)) * radian);  x.add(1, (a0.get("lng") + h0.get("lng") * tl.get(0)) * radian);
      x.add(2, (a0.get("lat") + h0.get("lat") * tl.get(1)) * radian);  x.add(3, (a0.get("lng") + h0.get("lng") * tl.get(1)) * radian);
      System.out.println(x.toString());
    } else {
      System.err.println("tl.size() == " + tl.size() + " !");
    }
  }
  
  /* public static List<Double> transposeMatrix(List<Double> m) {
    // first signature double[][] m , but code of the function has not been changed since then
    double[][] temp = new double[m[0].length][m.length];
    for (int i = 0; i < m.length; i++)
      for (int j = 0; j < m[0].length; j++)
        temp[j][i] = m[i][j];
    return temp;
  } */

}
