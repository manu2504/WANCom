import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public class RootHandler implements HttpHandler {
	
	private int port;
	private String pathHeader = "/";
	
	public RootHandler(int port) {
		super();
		this.port = port;
	}

     @Override
     public void handle(HttpExchange he) throws IOException {
    	 FileInputStream fis = new FileInputStream("/public_html/index.html");
//    	 InputStream is = he.getRequestBody();
    	 ServerSocket welcomeSocket = new ServerSocket(this.port);
    	 while (true) {
	    	 Socket connectionSocket = welcomeSocket.accept();
	    	 Thread httpw = new HttpWorker(connectionSocket, pathHeader);
	    	 httpw.start();
    	 }
    	 
//         String response = "<h1>Server start success " +
//         "if you see this message</h1>" + "<h1>Port: " + this.port + "</h1>";
//         he.sendResponseHeaders(200, 0);
//         OutputStream os = he.getResponseBody();
//         outputFile(fis, os);
//         os.close();
     }

     /**
      * This method writes the content of the file "f" in the output buffer "out"
      * @param f : file to copy
      * @param out : output buffer into which to copy the content of the file
      */
     static void outputFile(FileInputStream f, OutputStream out) throws IOException {
         while (true) {
             // Le fichier est lu ligne par ligne
             int line = f.read();
             if (line == -1) {
                 break; // Fin du fichier
             }
             out.write(line);
         }
     }

}