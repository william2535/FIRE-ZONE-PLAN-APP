package com.zonesketch.app;

import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private static final int PICK_IMAGE = 10;
    private ValueCallback<Uri[]> imageCallback;
    private Uri cameraOutput;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        WebView web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(true);
        web.addJavascriptInterface(new Bridge(), "AndroidBridge");
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (imageCallback != null) imageCallback.onReceiveValue(null);
                imageCallback = callback;
                cameraOutput = null;
                String[] accepted = params.getAcceptTypes();
                boolean json = false, pdf = false;
                for (String type : accepted) { if (type.contains("json")) json = true; if (type.contains("pdf")) pdf = true; }
                try {
                    if (params.isCaptureEnabled() && !json && !pdf) {
                        File folder = new File(getCacheDir(), "captures");
                        if (!folder.isDirectory() && !folder.mkdirs()) throw new IllegalStateException("Camera folder unavailable");
                        File[] oldPhotos = folder.listFiles();
                        if (oldPhotos != null) for (File old : oldPhotos) if (System.currentTimeMillis() - old.lastModified() > 86400000L) old.delete();
                        File photo = File.createTempFile("device_", ".jpg", folder);
                        cameraOutput = Uri.parse("content://com.zonesketch.app.share/capture/" + photo.getName());
                        Intent camera = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                        camera.putExtra(android.provider.MediaStore.EXTRA_OUTPUT, cameraOutput);
                        camera.setClipData(ClipData.newRawUri("Device photo", cameraOutput));
                        camera.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                        startActivityForResult(camera, PICK_IMAGE);
                    } else {
                        Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
                        pick.addCategory(Intent.CATEGORY_OPENABLE);
                        pick.setType(json || pdf ? "*/*" : "image/*");
                        if (pdf && !json) pick.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"image/*", "application/pdf"});
                        startActivityForResult(Intent.createChooser(pick, "Choose image or project"), PICK_IMAGE);
                    }
                } catch (Exception e) {
                    imageCallback.onReceiveValue(null); imageCallback = null; cameraOutput = null;
                    Toast.makeText(MainActivity.this, "Could not open camera or file picker. Try Choose photo instead.", Toast.LENGTH_LONG).show();
                }
                return true;
            }
        });
        try (InputStream in = getAssets().open("index.html"); ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192]; int n;
            while ((n = in.read(buffer)) != -1) bytes.write(buffer, 0, n);
            String html = bytes.toString(StandardCharsets.UTF_8.name());
            // An HTTPS base origin gives IndexedDB a stable, private origin. No network permission is requested.
            web.loadDataWithBaseURL("https://zonesketch.local/", html, "text/html", "UTF-8", null);
        } catch (Exception e) { Toast.makeText(this, "Could not load Zone Sketch by Will", Toast.LENGTH_LONG).show(); }
    }

    @Override protected void onActivityResult(int code, int result, Intent data) {
        super.onActivityResult(code, result, data);
        if (code == PICK_IMAGE && imageCallback != null) {
            Uri uri = result == RESULT_OK ? (cameraOutput != null ? cameraOutput : data != null ? data.getData() : null) : null;
            if (cameraOutput != null) revokeUriPermission(cameraOutput, Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            cameraOutput = null;
            imageCallback.onReceiveValue(uri == null ? null : new Uri[]{uri});
            imageCallback = null;
        }
    }

    private final class Bridge {
        @JavascriptInterface public void openBetaPortal() {
            runOnUiThread(() -> {
                try {
                    Intent open = new Intent(Intent.ACTION_VIEW, Uri.parse("https://william2535.github.io/FIRE-ZONE-PLAN-APP/beta.html"));
                    startActivity(open);
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "Could not open the beta tester portal", Toast.LENGTH_LONG).show();
                }
            });
        }
        @JavascriptInterface public void sharePng(String dataUrl, String suggestedName) {
            shareFile(dataUrl, suggestedName, "image/png");
        }
        @JavascriptInterface public void shareFile(String dataUrl, String suggestedName, String mime) {
            try {
                if (!mime.equals("image/png") && !mime.equals("application/pdf") && !mime.equals("application/json")) throw new IllegalArgumentException("Unsupported file type");
                int comma = dataUrl.indexOf(',');
                if (comma < 0 || !dataUrl.substring(0, comma).endsWith(";base64")) throw new IllegalArgumentException("Invalid export");
                byte[] bytes = Base64.decode(dataUrl.substring(comma + 1), Base64.DEFAULT);
                if (bytes.length == 0 || bytes.length > 64 * 1024 * 1024) throw new IllegalArgumentException("Export size");
                File folder = new File(getCacheDir(), "exports");
                if (!folder.isDirectory() && !folder.mkdirs()) throw new IllegalStateException("Export folder");
                File[] previous = folder.listFiles();
                if (previous != null) for (File old : previous) if (System.currentTimeMillis() - old.lastModified() > 7L * 24 * 60 * 60 * 1000) old.delete();
                final String filename = suggestedName.replaceAll("[^a-zA-Z0-9._-]", "_");
                File file = new File(folder, java.util.UUID.randomUUID().toString() + "_" + filename);
                try (FileOutputStream out = new FileOutputStream(file)) { out.write(bytes); }
                final Uri uri = Uri.parse("content://com.zonesketch.app.share/export/" + file.getName());
                runOnUiThread(() -> {
                    try {
                        Intent send = new Intent(Intent.ACTION_SEND);
                        send.setType(mime);
                        send.putExtra(Intent.EXTRA_STREAM, uri);
                        send.setClipData(ClipData.newUri(getContentResolver(), filename, uri));
                        send.putExtra(Intent.EXTRA_SUBJECT, filename);
                        send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                        startActivity(Intent.createChooser(send, "Send Zone Sketch by Will file"));
                    } catch (Exception e) { Toast.makeText(MainActivity.this, "No app available to share this file", Toast.LENGTH_LONG).show(); }
                });
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Could not export this file", Toast.LENGTH_LONG).show());
            }
        }
    }
}
