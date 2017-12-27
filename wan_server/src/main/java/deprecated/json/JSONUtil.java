package net.wancom.json;

import net.wancom.exceptions.WanComException;
import org.eclipse.persistence.jaxb.UnmarshallerProperties;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import javax.xml.transform.stream.StreamSource;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 * This class will read JSON data from the file and convert it to JSON objects for further processing in java.
 * We have a @see{{@link JSONCountry}} that we unmarshall the json files to this type of object.
 */
public class JSONUtil {

    private static final String APPLICATION_JSON = "application/json";

    /**
     * The method get the countryName, and the json file's name should be [countryName].json, so the method can read it.
     *
     * @param countryName
     * @return an object of type JSONCountry with all nodes and links
     */
    public static JSONCountry unmarshalJsonCountry(String countryName) {

        /* START: Finding json file */
        //class loader to find json files, you can have another solution for this part, the only goal is to find and read json files.
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        File jsonFile = new File(classLoader.getResource("public/" + countryName + ".json").getFile());
        /* END: Finding json file */
        try {
            //We have to set which contextFactory the application should use, otherwise it can be some kind of api conflict.
            System.setProperty("javax.xml.bind.context.factory", "org.eclipse.persistence.jaxb.JAXBContextFactory");
            //To unmarshall (json to java) we need a jaxbContext
            JAXBContext context = JAXBContext.newInstance(JSONCountry.class);

            //then an unmarshaller
            Unmarshaller unmarshaller = context.createUnmarshaller();

            //it is a json file we need to unmarshal, here we set the media type to json
            unmarshaller.setProperty(UnmarshallerProperties.MEDIA_TYPE, APPLICATION_JSON);
            unmarshaller.setProperty(UnmarshallerProperties.JSON_INCLUDE_ROOT, false);
            if (jsonFile.exists()) {
                InputStream inputStream = new FileInputStream(jsonFile);
                StreamSource streamSource = new StreamSource(inputStream);

                JSONCountry country = unmarshaller.unmarshal(streamSource, JSONCountry.class).getValue();
                return country;
            }
        } catch (JAXBException je) {
            throw new WanComException("There is a problem with converting JSON data to java object:: " + je.getMessage());
        } catch (FileNotFoundException fe) {
            throw new WanComException("The following file does not exists: \"" + jsonFile.getName() + "\"" + ". Error message :: " + fe.getMessage());
        }
        return null;
    }
}
