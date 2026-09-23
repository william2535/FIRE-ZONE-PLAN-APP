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
                Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
                pick.addCategory(Intent.CATEGORY_OPENABLE);
                pick.setType("image/*");
                try { startActivityForResult(Intent.createChooser(pick, "Choose floor plan image"), PICK_IMAGE); }
                catch (Exception e) { imageCallback.onReceiveValue(null); imageCallback = null; Toast.makeText(MainActivity.this, "No image picker available", Toast.LENGTH_LONG).show(); }
                return true;
            }
        });
        try (InputStream in = getAssets().open("index.html"); ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192]; int n;
            while ((n = in.read(buffer)) != -1) bytes.write(buffer, 0, n);
            String html = bytes.toString(StandardCharsets.UTF_8.name());
            // An HTTPS base origin gives IndexedDB a stable, private origin. No network permission is requested.
            web.loadDataWithBaseURL("https://zonesketch.local/", html, "text/html", "UTF-8", null);
        } catch (Exception e) { Toast.makeText(this, "Could not load Zone Sketch", Toast.LENGTH_LONG).show(); }
    }

    @Override protected void onActivityResult(int code, int result, Intent data) {
        super.onActivityResult(code, result, data);
        if (code == PICK_IMAGE && imageCallback != null) {
            Uri uri = result == RESULT_OK && data != null ? data.getData() : null;
            imageCallback.onReceiveValue(uri == null ? null : new Uri[]{uri});
            imageCallback = null;
        }
    }

    private final class Bridge {
        @JavascriptInterface public void sharePng(String dataUrl, String suggestedName) {
            try {
                int comma = dataUrl.indexOf(',');
                if (comma < 0 || !dataUrl.startsWith("data:image/png;base64,")) throw new IllegalArgumentException("Invalid image");
                byte[] png = Base64.decode(dataUrl.substring(comma + 1), Base64.DEFAULT);
                File file = new File(getCacheDir(), "shared-zone-draft.png");
                try (FileOutputStream out = new FileOutputStream(file)) { out.write(png); }
                final String filename = suggestedName.replaceAll("[^a-zA-Z0-9._-]", "_");
                runOnUiThread(() -> {
                    Intent send = new Intent(Intent.ACTION_SEND);
                    send.setType("image/png");
                    send.putExtra(Intent.EXTRA_STREAM, Uri.parse("content://com.zonesketch.app.share/draft.png"));
                    send.setClipData(ClipData.newUri(getContentResolver(), "Zone layout draft", Uri.parse("content://com.zonesketch.app.share/draft.png")));
                    send.putExtra(Intent.EXTRA_SUBJECT, filename);
                    send.putExtra(Intent.EXTRA_TEXT, "Zone layout site draft for office CAD redraw. Please verify on site.");
                    send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    startActivity(Intent.createChooser(send, "Send draft to office"));
                });
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Could not export the PNG", Toast.LENGTH_LONG).show());
            }
        }
    }
}
