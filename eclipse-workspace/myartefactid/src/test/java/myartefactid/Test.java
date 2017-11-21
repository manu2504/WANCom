package myartefactid;

/** We use Spark, a framework designed for web servers, to avoid coding the
 *  basic components of the web server
 *  http://sparkjava.com/documentation
**/
import static spark.Spark.*;

public class Test {

	public static void main(String[] args) {
		staticFiles.location("public"); // Static files
		get("/hello", (request, response) -> "Hello guys!");
		System.out.println("Server listening on port 4567");
		post("/sendmedata", (request, response) -> {
			System.out.println("data received " + request.body());
			return "{ \"lat\": 123.0, \"lng\": 146.0 }";
		});
	}

}
