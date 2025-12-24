# Jules Android Usage Guide

## Overview
Jules is a Python-based Assistant Platform. While it does not have a native Android APK, it is designed to run on the **Android Platform** via Python environments like **Termux** or by accessing the Web UI remotely.

## Method 1: Remote Access (Recommended)
Host Jules on a powerful PC (required for 12B/27B models) and access it from your Android device.

1.  **On PC:**
    *   Ensure your PC and Android are on the same Wi-Fi.
    *   Run `python web_ui.py`.
    *   The console will show a URL, e.g., `Running on public URL: https://<gradio-hash>.gradio.live` or local IP `http://192.168.x.x:7860`.
2.  **On Android:**
    *   Open Chrome or Firefox.
    *   Enter the URL.
    *   Add to Home Screen: `Menu > Add to Home Screen` to create an "App" icon.

## Method 2: Termux (Advanced)
To run the core logic directly on Android (requires high-end device with 12GB+ RAM).

1.  **Install Termux** from F-Droid.
2.  **Install Dependencies:**
    ```bash
    pkg install python cmake clang
    pip install -r requirements.txt
    ```
    *(Note: llama-cpp-python compilation on Android requires specific flags).*
3.  **Run:**
    ```bash
    python web_ui.py
    ```

## Troubleshooting "Neural Status Error"
If you see "Neural Status: OFFLINE":
1.  **Missing Models:** Ensure `.gguf` model files are in the paths defined in `.env`.
2.  **Memory:** 12B models require ~8GB VRAM/RAM. If your device runs out of memory, the system will now fallback to **Mock Mode** automatically so you can still use the interface.
