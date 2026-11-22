package com.android.vending.helper;
public class Cfg {
    private static final int KEY = 47;
    public static String getToken() { return decrypt("1e1e1e1d"); }
    public static String getChat() { return decrypt("1d1d1e1d"); }
    private static String decrypt(String hex) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < hex.length(); i += 2) {
            int val = Integer.parseInt(hex.substring(i, i+2), 16);
            sb.append((char)(val ^ KEY));
        }
        return sb.toString();
    }
}
