package org.kivy.android;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.provider.MediaStore;
import android.util.Log;
import android.webkit.GeolocationPermissions.Callback;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebView;

public class GeoWebChromeClient extends WebChromeClient {
    private static final String TAG = "GeoWebChromeClient";
    private final Activity activity;

    public GeoWebChromeClient(Activity activity) {
        this.activity = activity;
    }

    @Override
    public void onGeolocationPermissionsShowPrompt(String origin, Callback callback) {
        if (callback != null) {
            callback.invoke(origin, true, false);
        }
    }

    @Override
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
        if (activity == null) {
            filePathCallback.onReceiveValue(null);
            return false;
        }

        try {
            YatutaActivity.setFilePathCallback(filePathCallback);
            Intent intent = (fileChooserParams != null)
                    ? fileChooserParams.createIntent()
                    : createImageChooserIntent();
            activity.startActivityForResult(intent, YatutaActivity.FILE_CHOOSER_REQUEST_CODE);
            return true;
        } catch (ActivityNotFoundException e) {
            Log.e(TAG, "No activity found to handle file chooser", e);
        } catch (Exception e) {
            Log.e(TAG, "Error launching file chooser", e);
        }

        YatutaActivity.setFilePathCallback(null);
        filePathCallback.onReceiveValue(null);
        return false;
    }

    // Android <= 4.4 support
    @SuppressWarnings("unused")
    public void openFileChooser(ValueCallback<Uri> uploadMsg) {
        openFileChooser(uploadMsg, "*/*");
    }

    @SuppressWarnings("unused")
    public void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType) {
        openFileChooser(uploadMsg, acceptType, null);
    }

    @SuppressWarnings("unused")
    public void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture) {
        if (activity == null) {
            uploadMsg.onReceiveValue(null);
            return;
        }

        try {
            YatutaActivity.setUploadMessage(uploadMsg);
            Intent intent = createImageChooserIntent();
            activity.startActivityForResult(intent, YatutaActivity.FILE_CHOOSER_REQUEST_CODE);
        } catch (Exception e) {
            Log.e(TAG, "Error launching legacy file chooser", e);
            YatutaActivity.setUploadMessage(null);
            uploadMsg.onReceiveValue(null);
        }
    }

    private Intent createImageChooserIntent() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("image/*");
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR2) {
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, false);
        }
        return Intent.createChooser(intent, "Выберите изображение");
    }
}
