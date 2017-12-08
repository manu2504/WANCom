package net.wancom.wan_server;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class IntersectionPoint {
  
  // This Java code has been translated from the R code located here:
  // https://gis.stackexchange.com/questions/36841/line-intersection-with-circle-on-a-sphere-globe-or-earth#answer-36979
  
  /*
   * This function seeks to find the point of intersection between a circle centered around by (lat, lng)
   * and a (curved) line defined by two locations (lat, lng)
   */


  /*
   * Calculates and prints the coordinates of the point of intersection
   */
  public static void test() {
    double r; // radius (in km)
    double alpha, beta, gamma;
    Map<String, Double> a0, b0, c0, A, B, C, u, v, t, y, z, h0;
    
    // Constants
    double degree = 2.0 * Math.PI / 360.0;
    double radian = 1.0 / degree;
    double radius = 6371007.2;
    
    a0 = b0 = c0 = A = B = C = u = v = t = y = z = h0 = new HashMap<String, Double>();
    
    // Input
    a0.put("lat", 48.139115 * degree);
    a0.put("lng", 11.578081 * degree); // Point A in (lat, lon)
    b0.put("lat", 48.146303 * degree);
    b0.put("lng", 11.593102 * degree); // Point B
    c0.put("lat", 48.137024 * degree);
    c0.put("lng", 11.575249 * degree); // Center
    r = 100.0 * 1000.0;
    
    // Projection
    A.put("lat", a0.get("lat") * 1 * radius);
    A.put("lng", a0.get("lng") * Math.cos(c0.get("lat")) * radius );
    B.put("lat", b0.get("lat") * 1 * radius);
    B.put("lng", b0.get("lng") * Math.cos(c0.get("lat")) * radius );
    C.put("lat", c0.get("lat") * 1 * radius);
    C.put("lng", c0.get("lng") * Math.cos(c0.get("lat")) * radius );
    
    // Compute coefficients of the quadratic equation
    v.put("lat", A.get("lat") - C.get("lat"));
    v.put("lng", A.get("lng") - C.get("lng"));
    u.put("lat", B.get("lat") - A.get("lat"));
    u.put("lng", B.get("lng") - A.get("lng"));
    alpha = Math.sqrt(u.get("lat")) + Math.sqrt(u.get("lng"));
    beta = u.get("lat") * v.get("lat") + u.get("lng") * v.get("lng");
    gamma = Math.sqrt(v.get("lat")) + Math.sqrt(v.get("lng")) - Math.sqrt(r);
    
    // Solve the equation.
    t.put("lat", ( -beta + Math.sqrt(Math.sqrt(beta) - alpha * gamma) ) / alpha );
    t.put("lng", ( -beta - Math.sqrt(Math.sqrt(beta) - alpha * gamma) ) / alpha);
    List<Double> tl = new ArrayList<Double>();
    if (t.get("lat") >= 0 && t.get("lat") <= 1) { // Limit the solution to arc a0-b0.
      tl.add(t.get("lat"));
    }
    if (t.get("lng") >= 0 && t.get("lng") <= 1) {
      tl.add(t.get("lng"));
    }
    
    // TODO: translate this R statement to Java:
    // x <- (a0 + (b0-a0) %o% t) * radian  // Columns are (lat, lon)
    
    // trial:
    h0.put("lat", b0.get("lat") - a0.get("lat"));
    h0.put("lng", b0.get("lng") - a0.get("lng"));
    y.put("lat", transposeMatrix(tl)); // TODO: transposeMatrix needs to return Array (not [][] like currently)
    double[][] x = new double[2][tl.size()];
  }
  
  public static List<Double> transposeMatrix(List<Double> m) {
    // first signature double[][] m , but code of the function has not been changed since then
    double[][] temp = new double[m[0].length][m.length];
    for (int i = 0; i < m.length; i++)
      for (int j = 0; j < m[0].length; j++)
        temp[j][i] = m[i][j];
    return temp;
  }

}
