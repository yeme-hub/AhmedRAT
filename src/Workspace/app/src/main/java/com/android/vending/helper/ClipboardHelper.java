package com.android.vending.helper;
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
