import java.io.*;
import java.net.Socket;

enum FileType {JPEG, GIF, HTML, XML,  JS, CSS, NONE}

/**
 * Cette classe traite une nouvelle requête du serveur
 */
public class HttpWorker extends Thread {

    private Socket socket = null;
    protected BufferedReader input = null;
    protected DataOutputStream output = null;
    private final String pathHeader;
    String clientSentence;


    public HttpWorker(Socket socket, String path_header) {
        super("HttpWorker");
        this.socket = socket;
        this.pathHeader = path_header;
    }


    public void run() {
    	try {
    		input = new java.io.BufferedReader(new InputStreamReader(socket.getInputStream()));
			output = new DataOutputStream(socket.getOutputStream());
			httpHandler();
			input.close();
			output.close();
			socket.close();
		} catch (IOException e) {
			System.err.println(e);
		}
    }


    /**
     *  Process an HTTP request
     */
    private void httpHandler() {
    	try {
    		clientSentence = input.readLine();
    	} catch (IOException e) {
    		System.err.println(e);
    	}
    	String[] clientCommand = clientSentence.split(" ");
    	//System.out.println("commande du client : " + clientCommand); // for debugging
    	String typeRequete = clientCommand[0];
    	//System.out.println("type requête : " + typeRequete); // for debugging
    	
    	if (typeRequete.equals("GET")) {
			String path = clientCommand[1];
			//System.out.println("path: " + path); // for debugging
			if (path.equals("/")) path = "index.html";
			if (path.startsWith("/")) path = path.substring(1);
			//System.out.println("path: " + path); // for debugging
			String pathRequested = this.pathHeader + path;
			System.out.println("pathRequested: " + pathRequested); // for debugging
			int i = path.lastIndexOf('.');
			String extension = "";
			if (i > 0) {
				extension = path.substring(i+1);
			}
			//System.out.println("extension : " + extension); // for debugging
			FileType filetype;
			switch (extension.toUpperCase()) {
				case "HTML":
					filetype = FileType.HTML;
					break;
				case "JPEG":
					filetype = FileType.JPEG;
	                break;
	            case "GIF":
					filetype = FileType.GIF;
	                break;
	            case "XML":
					filetype = FileType.XML;
	                break;
	            case "CSS":
					filetype = FileType.CSS;
	                break;
	            case "JS":
					filetype = FileType.JS;
	                break;
	            default:
					filetype = FileType.HTML;
			}
			File f = new File(pathRequested);
			FileInputStream fis;
			
			if (f.exists()) {
				if (!f.isDirectory()) {
					try {
						fis = new FileInputStream(pathRequested);
//						output.writeBytes(HttpServer.constructHttpHeader(200, filetype));
//						HttpServer.outputFile(fis, output);
					} catch (IOException e) {
						System.err.println(e);
					}
				} else {
					try {
						if (!pathRequested.endsWith("/")) {
							pathRequested += "/";
						}
						fis = new FileInputStream(pathRequested + "index.html");
//						output.writeBytes(HttpServer.constructHttpHeader(200, FileType.HTML));
//						HttpServer.outputFile(fis, output);
					} catch (IOException e) {
						System.err.println(e);
					}
				}
			} else {
				fileNotFoundHandler(pathRequested);
			}
		}
    }


    /** This method handles a resource nowhere to be found
     * @param path : path of the resource not found
     */
    public void fileNotFoundHandler(String path) {
        try {
            // Sending a 404 error : File not found
            String retMessage = "<html><head></head><body>Fichier "+path+" non trouvé...</body></html>\n";

//            output.writeUTF(HttpServer.constructHttpHeader(404, FileType.HTML));
            output.writeUTF(retMessage);
        } catch (Exception e) {
            System.err.println("Erreur avec le chemin "+path+" : " + e.getMessage());
        }
    }

} // class
