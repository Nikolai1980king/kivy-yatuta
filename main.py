"""
Yatuta Kivy application that wraps https://ятута.рф inside an Android WebView.
Includes Android-specific glue for geolocation and image upload.
"""

from __future__ import annotations

import os
import time
import traceback

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

WEBSITE_URL = os.getenv("WEBSITE_URL", "https://ятута.рф")


def log_error(message: str, error: Exception | None = None) -> None:
    """Centralised logging helper (prints + Android logcat when available)."""
    prefix = "[YatutaApp]"
    try:
        if platform == "android":
            from jnius import autoclass  # type: ignore  # pylint: disable=import-error

            Log = autoclass("android.util.Log")  # type: ignore
            if error:
                Log.e("YatutaApp", f"{message}: {error}")
                Log.e("YatutaApp", traceback.format_exc())
            else:
                Log.i("YatutaApp", message)
    except Exception:  # noqa: broad-except - log best-effort
        pass

    if error:
        print(f"{prefix} {message}: {error}")
        traceback.print_exc()
    else:
        print(f"{prefix} {message}")


if platform == "android":
    try:
        from android.permissions import (  # type: ignore  # pylint: disable=import-error
            Permission,
            request_permissions,
        )
    except ImportError:
        request_permissions = None
        Permission = None
    else:
        base_permissions = [
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
        ]
        if hasattr(Permission, "READ_MEDIA_IMAGES"):
            base_permissions.append(Permission.READ_MEDIA_IMAGES)
        if hasattr(Permission, "READ_EXTERNAL_STORAGE"):
            base_permissions.append(Permission.READ_EXTERNAL_STORAGE)
        if request_permissions:
            request_permissions(base_permissions)

    from jnius import autoclass  # type: ignore  # pylint: disable=import-error

    WebView = autoclass("android.webkit.WebView")
    WebViewClient = autoclass("android.webkit.WebViewClient")
    WebSettings = autoclass("android.webkit.WebSettings")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    View = autoclass("android.view.View")
    PythonActivity = autoclass("org.kivy.android.YatutaActivity")
    GeoWebChromeClient = autoclass("org.kivy.android.GeoWebChromeClient")
    WebChromeClient = autoclass("android.webkit.WebChromeClient")

    class AndroidWebView(BoxLayout):
        def __init__(self, url: str, **kwargs) -> None:
            super().__init__(**kwargs)
            self.url = url
            self.webview = None
            self.geo_client = None
            self.retry_count = 0
            self.max_retries = 10
            Clock.schedule_once(lambda *_: self._setup_webview(), 2.0)

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------
        def _get_activity_safe(self):
            try:
                activity = getattr(PythonActivity, "mActivity", None)
            except Exception:  # noqa: broad-except
                activity = None

            if activity is None:
                try:
                    activity = (
                        PythonActivity.getCurrentActivity()  # type: ignore[attr-defined]
                        if hasattr(PythonActivity, "getCurrentActivity")
                        else None
                    )
                except Exception:  # noqa: broad-except
                    activity = None

            if not activity:
                return None

            try:
                window = activity.getWindow()
                if window is None:
                    return None
            except Exception:  # noqa: broad-except
                return None

            return activity

        def _run_on_ui(self, activity, func):
            activity.runOnUiThread(func)

        def _show_error(self, message: str) -> None:
            from kivy.uix.label import Label

            self.clear_widgets()
            self.add_widget(
                Label(
                    text=message,
                    halign="center",
                    valign="middle",
                    padding=(20, 20),
                )
            )

        # ------------------------------------------------------------------
        # WebView lifecycle
        # ------------------------------------------------------------------
        def _setup_webview(self, *_):
            activity = self._get_activity_safe()
            if activity is None:
                self.retry_count += 1
                if self.retry_count < self.max_retries:
                    log_error("Activity not ready yet, retrying...")
                    Clock.schedule_once(lambda *_: self._setup_webview(), 1.0)
                else:
                    self._show_error("Не удалось получить Activity")
                return

            result = {"view": None, "error": None}

            def create_view():
                try:
                    result["view"] = WebView(activity)
                except Exception as exc:  # noqa: broad-except
                    result["error"] = exc

            self._run_on_ui(activity, create_view)
            time.sleep(0.3)

            webview = result["view"]
            if webview is None:
                try:
                    Context = autoclass("android.content.Context")
                    app_ctx = activity.getApplicationContext()
                    if app_ctx:
                        webview = WebView(app_ctx)
                except Exception as exc:  # noqa: broad-except
                    result["error"] = exc

            if webview is None:
                log_error("WebView creation failed", result["error"])
                self._show_error("Не удалось создать WebView")
                return

            self._continue_webview_setup(webview, activity)

        def _continue_webview_setup(self, webview, activity) -> None:
            webview_client = WebViewClient()

            def configure():
                try:
                    settings = webview.getSettings()
                    settings.setJavaScriptEnabled(True)
                    settings.setDomStorageEnabled(True)
                    settings.setDatabaseEnabled(True)
                    settings.setAllowFileAccess(True)
                    settings.setAllowContentAccess(True)
                    settings.setSupportZoom(True)
                    settings.setBuiltInZoomControls(True)
                    settings.setDisplayZoomControls(False)

                    try:
                        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW)
                    except Exception:  # noqa: broad-except
                        pass

                    try:
                        settings.setGeolocationEnabled(True)
                        geo_path = activity.getDir("database", 0).getPath()
                        settings.setGeolocationDatabasePath(geo_path)
                    except Exception as exc:  # noqa: broad-except
                        log_error("Geolocation setting failed", exc)

                    webview.setWebViewClient(webview_client)

                    if self.geo_client is None:
                        try:
                            self.geo_client = GeoWebChromeClient(activity)
                        except Exception as exc:  # noqa: broad-except
                            log_error("GeoWebChromeClient creation failed", exc)
                            self.geo_client = None

                    if self.geo_client is not None:
                        webview.setWebChromeClient(self.geo_client)
                    else:
                        webview.setWebChromeClient(WebChromeClient())

                    self.webview = webview

                    layout_params = LayoutParams(-1, -1)
                    root_view = None
                    try:
                        R = autoclass("android.R")
                        root_view = activity.findViewById(R.id.content)
                    except Exception:  # noqa: broad-except
                        try:
                            window = activity.getWindow()
                            root_view = window.getDecorView() if window else None
                        except Exception:  # noqa: broad-except
                            root_view = None

                    if root_view is not None:
                        try:
                            root_view.addView(webview, layout_params)
                        except Exception:
                            activity.addContentView(webview, layout_params)
                    else:
                        activity.addContentView(webview, layout_params)

                    webview.setVisibility(View.VISIBLE)
                    webview.bringToFront()
                    webview.requestFocus()
                    webview.loadUrl(self.url)
                except Exception as exc:  # noqa: broad-except
                    log_error("setup_webview_in_ui failed", exc)
                    self._show_error("Ошибка настройки WebView")

            self._run_on_ui(activity, configure)
            Clock.schedule_once(lambda *_: self._post_setup(activity), 2.0)

        def _post_setup(self, activity) -> None:
            if not self.webview:
                return

            def check_visibility():
                try:
                    visibility = self.webview.getVisibility()
                    log_error(f"WebView visibility: {visibility}")
                    Clock.schedule_once(lambda *_: self._hide_kivy_window(), 3.0)
                except Exception as exc:  # noqa: broad-except
                    log_error("Visibility check failed", exc)

            self._run_on_ui(activity, check_visibility)

        # ------------------------------------------------------------------
        # Public helpers
        # ------------------------------------------------------------------
        def reload(self):
            if self.webview:
                self.webview.reload()

        def go_back(self):
            if self.webview and self.webview.canGoBack():
                self.webview.goBack()

        def go_forward(self):
            if self.webview and self.webview.canGoForward():
                self.webview.goForward()

        def _hide_kivy_window(self):
            activity = self._get_activity_safe()
            if not activity or not self.webview:
                return

            def hide():
                try:
                    self.webview.bringToFront()
                    self.webview.setVisibility(View.VISIBLE)
                    self.webview.requestFocus()
                except Exception as exc:  # noqa: broad-except
                    log_error("Failed to bring WebView to front", exc)
                try:
                    Window.hide()
                except Exception as exc:  # noqa: broad-except
                    log_error("Failed to hide Window", exc)

            self._run_on_ui(activity, hide)

else:  # Non-Android platforms -------------------------------------------------
    from kivy.uix.label import Label

    class AndroidWebView(BoxLayout):
        def __init__(self, url: str, **kwargs) -> None:
            super().__init__(**kwargs)
            self.orientation = "vertical"
            self.add_widget(
                Label(
                    text=f"Для тестирования откройте сайт вручную:\n{url}",
                    halign="center",
                )
            )


class YatutaApp(App):
    def build(self):
        try:
            Window.clearcolor = (0, 0, 0, 0)
            layout = BoxLayout(orientation="vertical")
            layout.add_widget(AndroidWebView(WEBSITE_URL))
            return layout
        except Exception as exc:  # noqa: broad-except
            log_error("Error in build()", exc)
            from kivy.uix.label import Label

            error_text = f"Ошибка запуска:\n{exc}\n\n{traceback.format_exc()[:200]}"
            return Label(
                text=error_text,
                halign="center",
                valign="middle",
                padding=(20, 20),
            )

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    try:
        YatutaApp().run()
    except Exception as exc:  # noqa: broad-except
        log_error("Fatal error in main", exc)
