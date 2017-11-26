package net.wancom.wan_server;

import static spark.Spark.*;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args ) {
      staticFiles.location("public"); // Static files
      get("/hello", (request, response) -> "Hello guys!");
      System.out.println("Server listening on port 4567");
      post("/sendmedata", (request, response) -> {
        System.out.println("data received " + request.body());
        return "{ \"lat\": 123.0, \"lng\": 146.0 }";
      });
    }
}
