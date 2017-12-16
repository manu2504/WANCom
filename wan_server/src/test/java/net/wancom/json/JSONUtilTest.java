package net.wancom.json;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class JSONUtilTest {

    @Test
    public void unmarshalJsonCountry() {
        String china = "China";
        JSONCountry country = JSONUtil.unmarshalJsonCountry(china);
        assertNotNull(country);
        assertEquals(38, country.getNodes().size());
        assertEquals(62, country.getLinks().size());
        
        //The test can be extended to other countries to see if json unmarshalling method read the data correctly
    }
}