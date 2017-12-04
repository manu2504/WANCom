/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author biwen
 */
import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import org.apache.commons.io.FileUtils;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;




public class ReadJson {
    
    
    
    
    public static void  main(String[] args) throws IOException, JSONException {
        // Reading from System.in
        double ax;
        double ox;
        double ay = 0;
        double oy = 0;
        double az = 0;
        double oz = 0;
        
        File file = new File (ReadJson.class.getResource("/Uunet.json").getFile());
        
        String content=FileUtils.readFileToString(file);
        JSONObject jsonObject = new JSONObject(content);
        JSONArray nodes = jsonObject.getJSONArray("nodes");
        System.out.println("please enter first three hops of you original path ");
        Scanner reader = new Scanner(System.in);
        System.out.println("Enter hopa: ");
        String x = reader.nextLine();
        System.out.println("Enter hopb ");
        String y = reader.nextLine();
        System.out.println("Enter hopc ");
        String z = reader.nextLine();
        
        Scanner in = new Scanner(System.in);
        reader.close();
        
        for (int index = 0; index < nodes.length(); ++index)
        {
            JSONObject node = nodes.getJSONObject(index);
            
            
            
            if(node.getString("id") == null ? x == null : node.getString("id").equals(x)){
                
                String lonx = node.getString("Longitude");
                String lanx =node.getString("Latitude");
                System.out.println(lonx);
                System.out.println(lanx);
                
                ax= Double.parseDouble(lanx);
                
                ox= Double.parseDouble(lonx);
                
            }
            
            
            
            else if (node.getString("id") == null ? y == null : node.getString("id").equals(y)){
                //if("Vancouver".equals(node.getString("id"))){
                
                String lony = node.getString("Longitude");
                String lany =  node.getString("Latitude");
                ay= Double.parseDouble(lany);
                oy= Double.parseDouble(lony);
                System.out.println(lony);
                System.out.println(lany);
                
                
                
                
            }
            
            
            else if(node.getString("id") == null ? z == null : node.getString("id").equals(z)){
                //if("Vancouver".equals(node.getString("id"))){
                
                String lonz = node.getString("Longitude");
                oz= Double.parseDouble(lonz);
                String lanz = node.getString("Latitude");
                az= Double.parseDouble(lanz);
                System.out.println(lonz);
                System.out.println(lanz);
                
                
                
                
                
            }
            else{
                System.out.println();
                
            }
            
            
        }
        
        double lontitudenew=  (oz/0.5 )+(oy * -0.5/0.5);
        double latitudenew=  (az/0.5 )+ (ay * -0.5/0.5);
        
        System.out.println(lontitudenew);
        System.out.println(latitudenew);
        
        
        //node0[Longitude] = node2[Longitude]/n + node3[Longitude]*(n-1)/n (1<n<someting)
        
    }
    
    
    
    
    
    
}



