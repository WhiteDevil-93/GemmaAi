import os
import subprocess
import sys

# --- CONFIGURATION ---
PROJECT_NAME = "assistant-platform"

# --- FIXED REQUIREMENTS (Pinned to stop the loop) ---
REQUIREMENTS = """
llama-cpp-python>=0.2.77
numpy<2.0.0
pydantic>=2.0
gradio>=4.0.0
# Pinned for Windows Stability to stop the backtracking
chromadb==0.4.24
llama-index-core==0.10.18
llama-index-embeddings-huggingface==0.2.0
llama-index-vector-stores-chroma==0.1.6
python-dotenv
pyyaml
colorama
"""

def jules_execute():
    print(">> JULES: DETECTED DEPENDENCY LOOP. APPLYING SURGICAL FIX...")
    
    # 1. Overwrite requirements.txt with stable pinned versions
    req_path = os.path.join(PROJECT_NAME, "requirements.txt")
    with open(req_path, "w", encoding="utf-8") as f:
        f.write(REQUIREMENTS.strip())
    print("✔ Requirements pinned for stability.")

    # 2. Force Install
    print(">> INSTALLING (This will be fast)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])

    # 3. Launch Web UI
    print(">> LAUNCHING CONTROL ROOM...")
    ui_path = os.path.join(PROJECT_NAME, "web_ui.py")
    subprocess.run([sys.executable, ui_path])

if __name__ == "__main__":
    jules_execute()
