package deprecated.json;

import java.util.List;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class JSONCountry {
    private List<JSONNode> nodes;
    private List<JSONLink> links;

    public List<JSONNode> getNodes() {
        return nodes;
    }

    public void setNodes(List<JSONNode> nodes) {
        this.nodes = nodes;
    }

    public List<JSONLink> getLinks() {
        return links;
    }

    public void setLinks(List<JSONLink> links) {
        this.links = links;
    }
}
