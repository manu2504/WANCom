import java.io.*;
import java.net.Socket;
import java.util.zip.Inflater;

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
        /* A compléter */
    	// on utilise la forme try-with pour profiter du fait que les
    	// classes BufferedReader, DataOutputStream et Socket implémentent
    	// l'interface AutoCloseable
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
     *  Traite une requête HTTP
     */
    private void httpHandler() {
        /* A compléter TODO continuer ici */
    	try {
    		clientSentence = input.readLine();
    	} catch (IOException e) {
    		System.err.println(e);
    	}
    	String[] clientCommand = clientSentence.split(" ");
    	//System.out.println("commande du client : " + clientCommand); // pour le debug
    	String typeRequete = clientCommand[0];
    	//System.out.println("type requête : " + typeRequete); // pour le debug
    	
    	if (typeRequete.equals("GET")) {
			String path = clientCommand[1];
			//System.out.println("path: " + path); // pour le debug
			if (path.equals("/")) path = "index.html";
			if (path.startsWith("/")) path = path.substring(1);
			//System.out.println("path: " + path); // pour le debug
			String pathRequested = this.pathHeader + path;
			System.out.println("pathRequested: " + pathRequested); // pour le debug
			int i = path.lastIndexOf('.');
			String extension = "";
			if (i > 0) {
				extension = path.substring(i+1);
			}
			//System.out.println("extension : " + extension); // pour le debug
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


    /** Cette méthode gère une ressource non trouvée
     * @param path : chemin de la ressource non trouvée
     */
    public void fileNotFoundHandler(String path) {
        try {
            // Envoi de l'erreur 404 : Fichier non trouvé
            String retMessage = "<html><head></head><body>Fichier "+path+" non trouvé...</body></html>\n";

//            output.writeUTF(HttpServer.constructHttpHeader(404, FileType.HTML));
            output.writeUTF(retMessage);
        } catch (Exception e) {
            System.err.println("Erreur avec le chemin "+path+" : " + e.getMessage());
        }
    }

} // class
