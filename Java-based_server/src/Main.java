import java.io.IOException;
import java.net.*;

import com.sun.net.httpserver.HttpServer;

public class Main {

	public static void main(String[] args) throws IOException {
		int port = 4444;

        HttpServer server;
		try {
			server = HttpServer.create(new InetSocketAddress(port), 0);
	        System.out.println("server started at " + port);
	        server.createContext("/public_html", new RootHandler(port));
	        server.setExecutor(null);
	        server.start();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
