package net.wancom.eics;

/*
 * Called in JSONUtils to calculate the distance between two nodes
 */
public class Distance {

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
}
