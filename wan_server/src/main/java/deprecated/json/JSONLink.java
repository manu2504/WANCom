package net.wancom.json;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class JSONLink {
    private String source;
    private String target;

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }

    @Override
    public String toString() {
        return "ClassPojo [source = " + source + ", target = " + target + "]";
    }
}
