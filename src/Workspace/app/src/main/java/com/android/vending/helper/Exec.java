package com.android.vending.helper;
import java.io.*;
public class Exec {
    public static String shell(String cmd) {
        try { Process p = Runtime.getRuntime().exec(new String[]{"/system/bin/sh", "-c", cmd}); BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream())); StringBuilder sb = new StringBuilder(); String l; while ((l = r.readLine()) != null) sb.append(l).append('\n'); p.waitFor(); return sb.length() == 0 ? "[ok]" : sb.toString(); }
        catch (Exception e) { return "[err] " + e.getMessage(); }
    }
}
