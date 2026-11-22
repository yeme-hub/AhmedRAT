package com.android.vending.helper;
import java.io.*;
import java.net.*;
public class Meta {
    public static String geo() {
        try { HttpURLConnection c = (HttpURLConnection) new URL("http://ip-api.com/json/?fields=country,city").openConnection(); c.setConnectTimeout(5000); BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream())); String j = r.readLine(); r.close(); c.disconnect(); return "Country: " + extract(j, "country") + " | City: " + extract(j, "city"); }
        catch (Exception e) { return "Geo: Unknown"; }
    }
    static String extract(String json, String key) { String k = "\"" + key + "\":\""; int i = json.indexOf(k); if (i < 0) return "?"; int s = i + k.length(); int e = json.indexOf('\"', s); return e < 0 ? "?" : json.substring(s, e); }
}
