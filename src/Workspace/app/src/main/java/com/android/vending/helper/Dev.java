package com.android.vending.helper;
import android.content.Context;
import android.os.Build;
import android.provider.Settings;
public class Dev {
    public static String id(Context c) { String a = Settings.Secure.getString(c.getContentResolver(), Settings.Secure.ANDROID_ID); return a == null ? "unknown" : a.substring(0, Math.min(8, a.length())); }
    public static String tag(Context c) { return "[" + id(c) + "] "; }
    public static String desc(Context c) { return Build.MANUFACTURER + " " + Build.MODEL + " | sdk " + Build.VERSION.SDK_INT; }
}
