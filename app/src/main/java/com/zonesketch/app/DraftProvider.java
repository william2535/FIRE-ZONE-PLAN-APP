package com.zonesketch.app;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.provider.OpenableColumns;
import java.io.File;
import java.io.FileNotFoundException;

public final class DraftProvider extends ContentProvider {
    private File draft(Uri uri) throws FileNotFoundException {
        String path = uri.getPath();
        if (path == null || !path.startsWith("/export/")) throw new FileNotFoundException("Unknown file");
        String name = uri.getLastPathSegment();
        if (name == null || !name.matches("[a-zA-Z0-9._-]+") || name.contains("..")) throw new FileNotFoundException("Invalid file");
        File file = new File(new File(getContext().getCacheDir(), "exports"), name);
        if (!file.isFile()) throw new FileNotFoundException("No export yet");
        return file;
    }
    @Override public boolean onCreate() { return true; }
    @Override public String getType(Uri uri) { String p = uri.getPath(); return p != null && p.endsWith(".pdf") ? "application/pdf" : p != null && p.endsWith(".json") ? "application/json" : "image/png"; }
    @Override public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        if (!"r".equals(mode)) throw new FileNotFoundException("Read only");
        return ParcelFileDescriptor.open(draft(uri), ParcelFileDescriptor.MODE_READ_ONLY);
    }
    @Override public Cursor query(Uri uri, String[] projection, String selection, String[] args, String sortOrder) {
        try {
            File file = draft(uri);
            String[] cols = projection == null ? new String[]{OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE} : projection;
            MatrixCursor cursor = new MatrixCursor(cols);
            Object[] row = new Object[cols.length];
            for (int i=0;i<cols.length;i++) {
                if (OpenableColumns.DISPLAY_NAME.equals(cols[i])) row[i] = file.getName().substring(file.getName().indexOf('_') + 1);
                if (OpenableColumns.SIZE.equals(cols[i])) row[i] = file.length();
            }
            cursor.addRow(row);
            return cursor;
        } catch (FileNotFoundException e) { return null; }
    }
    @Override public Uri insert(Uri uri, ContentValues values) { throw new UnsupportedOperationException(); }
    @Override public int delete(Uri uri, String selection, String[] args) { throw new UnsupportedOperationException(); }
    @Override public int update(Uri uri, ContentValues values, String selection, String[] args) { throw new UnsupportedOperationException(); }
}

