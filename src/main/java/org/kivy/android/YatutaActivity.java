package org.kivy.android;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.util.Log;
import android.webkit.ValueCallback;

import org.kivy.android.PythonActivity;

import java.util.ArrayList;
import java.util.List;

public class YatutaActivity extends PythonActivity {
    private static final String TAG = "YatutaActivity";
    public static final int FILE_CHOOSER_REQUEST_CODE = 10001;

    private static ValueCallback<Uri[]> filePathCallback;
    private static ValueCallback<Uri> uploadMessage;

    public static void setFilePathCallback(ValueCallback<Uri[]> callback) {
        filePathCallback = callback;
    }

    public static void setUploadMessage(ValueCallback<Uri> callback) {
        uploadMessage = callback;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != FILE_CHOOSER_REQUEST_CODE) {
            return;
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            if (filePathCallback == null) {
                return;
            }

            Uri[] results = null;
            if (resultCode == RESULT_OK) {
                results = extractUris(data);
            }

            filePathCallback.onReceiveValue(results);
            filePathCallback = null;
        } else {
            if (uploadMessage == null) {
                return;
            }

            Uri result = (data == null || resultCode != RESULT_OK) ? null : data.getData();
            uploadMessage.onReceiveValue(result);
            uploadMessage = null;
        }
    }

    private Uri[] extractUris(Intent data) {
        List<Uri> uris = new ArrayList<>();
        try {
            if (data == null) {
                return null;
            }

            if (data.getClipData() != null) {
                int count = data.getClipData().getItemCount();
                for (int i = 0; i < count; i++) {
                    Uri uri = data.getClipData().getItemAt(i).getUri();
                    if (uri != null) {
                        uris.add(uri);
                    }
                }
            } else if (data.getData() != null) {
                uris.add(data.getData());
            } else if (data.getDataString() != null) {
                uris.add(Uri.parse(data.getDataString()));
            }
        } catch (Exception e) {
            Log.e(TAG, "Failed to extract URIs", e);
        }

        if (uris.isEmpty()) {
            return null;
        }

        return uris.toArray(new Uri[0]);
    }
}

