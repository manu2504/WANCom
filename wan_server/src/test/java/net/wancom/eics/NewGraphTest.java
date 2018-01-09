package net.wancom.eics;

import net.wancom.GraphTestUtil;
import net.wancom.exceptions.WanComException;
import net.wancom.graph.Graph;
import net.wancom.json.JSONCountry;
import net.wancom.json.JSONUtil;
import org.junit.Before;
import org.junit.Test;

import deprecated.algorithm.NewGraph;

import java.util.Scanner;

import static org.junit.Assert.assertNotNull;

public class NewGraphTest {

    protected Scanner keyboard;
    protected String unimprovedCountry;
    protected Graph unimprovedGraph;

    @Before
    public void setUp() throws Exception {
        // Here we create a graph to evaluate the addBestNewNode (improved Graph).
        unimprovedCountry = "France";
        System.out.println("==== START ---- Before any improvement. COUNTRY :: " + unimprovedCountry);
        try {
            //Unfortunately we could not create a graph via JSONUtils and used the deprecetade one with unmarshaller
            //JSONObject jsonObject = JSONUtils.NewJSONTopologyFromJSONFile(unimprovedCountry);
            //unimprovedGraph = JSONUtils.graphFromJSONTopology(jsonObject); // First input of addNewBestNode
            JSONCountry jsonCountry = JSONUtil.unmarshalJsonCountry(unimprovedCountry);
            unimprovedGraph = GraphTestUtil.createTheGraph(jsonCountry);
        } catch (WanComException we) {
            System.out.println("There is a problem (finding the file or parsing the json) and graph cannot be created: " + we.getMessage());
            we.printStackTrace();
        } catch (Exception e) {
            System.out.println("Something went wrong: " + e.getMessage());
            e.printStackTrace();
        }
        System.out.println("==== END ---- Before any improvement :: ");
    }

    @Test
    public void EvaluateAddBestNewNode() throws Exception {

        //When this method is running, unimprovedGraph has been initiated in setUp method.
        //addBestNewNode(Graph graph, String country, int constraint)
        String improvementCountry = "Germany";
        Integer constraints = 200;
        long startTime = System.currentTimeMillis();
        NewGraph.addBestNewNode(unimprovedGraph, improvementCountry, constraints);
        long stopTime = System.currentTimeMillis();
        long elapsedTime = stopTime - startTime;
        System.out.println("Elapsed time of running improvement: " + elapsedTime + " miliseconds");
        assertNotNull(elapsedTime);

    }


}