import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class testwrite {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {

        // JSONObject countryObj = new JSONObject();
        // countryObj.put("Name", "India");
        //countryObj.put("Population", new Integer(1000000));

        //JSONArray listOfStates = new JSONArray();
        //listOfStates.add("Madhya Pradesh");
        //listOfStates.add("Maharastra");
        //listOfStates.add("Rajasthan");

        //countryObj.put("States", listOfStates);
        JSONArray jsonArray = new JSONArray();
        JSONObject jsonObj = new JSONObject();

        for (int i = 0; i < 10; i++) {

            jsonObj.put("source", i);
            jsonObj.put("target", i+1);
            jsonArray.add(jsonObj);

            JSONObject mainObj = new JSONObject();
            mainObj.put("links", jsonArray);
            try {

                // Writing to a file
                FileWriter file = new FileWriter("Testtest.json");
               file.append(mainObj.toJSONString());
               // FileWriter file = new FileWriter(file);
                System.out.println();
                System.out.print(mainObj.toJSONString());

              //  file.write(jsonArray.toJSONString());
                file.flush();
               file.close();

            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }
}