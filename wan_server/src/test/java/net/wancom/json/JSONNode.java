package net.wancom.json;

/**
 * Created by farzadha@kth.se on 2017-12-14.
 */
public class JSONNode {
    private String id;
    private double latitude;
    private int internal;
    private double longitude;
    private String country;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double Latitude) {
        this.latitude = Latitude;
    }

    public int getInternal() {
        return internal;
    }

    public void setInternal(int Internal) {
        this.internal = Internal;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double Longitude) {
        this.longitude = Longitude;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String Country) {
        this.country = Country;
    }

    @Override
    public String toString() {
        return "ClassPojo [id = " + id + ", latitude = " + latitude + ", internal = " + internal + ", longitude = " + longitude + ", country = " + country + "]";
    }
}
