package com.android.vending.helper;
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
