
import os

# --- CONFIGURATION ---
PROJECT_NAME = "assistant-platform"
PERSONA = "You are Jules, a Senior Clinical Toxicologist and AI Operations Manager. Direct, technical, and execution-focused."

# --- DIRECTORY STRUCTURE ---
DIRS = [
    f"{PROJECT_NAME}/app/core",        
    f"{PROJECT_NAME}/app/tools",       
    f"{PROJECT_NAME}/app/prompts",     
    f"{PROJECT_NAME}/app/schemas",     
    f"{PROJECT_NAME}/app/connectors",  
    f"{PROJECT_NAME}/data/input",      
    f"{PROJECT_NAME}/data/output",     
    f"{PROJECT_NAME}/data/vectors",    
    f"{PROJECT_NAME}/docs",
    f"{PROJECT_NAME}/tests",
]

# --- FILE CONTENTS ---
FILES = {
    # 1. REQUIREMENTS (Updated with Gradio for 'Her Website')
    f"{PROJECT_NAME}/requirements.txt": """
llama-cpp-python>=0.2.77
numpy
pydantic>=2.0
gradio>=4.0.0             # The Web Interface (Stage 9)
llama-index-core
llama-index-embeddings-huggingface
llama-index-vector-stores-chroma
python-dotenv
pyyaml
colorama
""",

    # 2. ENVIRONMENT CONFIG
    f"{PROJECT_NAME}/.env": f"""
GPU_LAYERS=28
CONTEXT_WINDOW=32768
THREADS=8
MODEL_PATH_CURATOR="C:/AI/Models/gemma-3-12b-it-qat-Q4_K_M.gguf"
MODEL_PATH_DEVOURER="C:/AI/Models/gemma-3-27b-it-qat-Q4_K_M.gguf"
SYSTEM_PROMPT="{PERSONA}"
""",

    # 3. GITIGNORE
    f"{PROJECT_NAME}/.gitignore": """
*.gguf
data/input/*
data/output/*
data/vectors/*
__pycache__/
.env
""",

    # 4. MAIN CLI (Skeleton)
    f"{PROJECT_NAME}/main.py": """
import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style

load_dotenv()
init()

def main():
    print(f"{Fore.CYAN}[JULES]{Style.RESET_ALL} Control Room CLI Active.")
    print("Run 'python web_ui.py' to launch the visual interface.")

if __name__ == "__main__":
    main()
""",

    # 5. HER WEBSITE (Gradio UI - Stage 9)
    f"{PROJECT_NAME}/web_ui.py": """
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "System Ready.")

def chat_logic(message, history):
    # This is where we hook into the Gemma 3 12B Model
    # For now, it returns a skeleton response to prove the UI works
    return f"[JULES]: Received. You said: {message} (Logic connecting to GPU...)"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🏥 Jules: Clinical AI Operations")
    gr.Markdown("> *Senior Toxicologist & Research Orchestrator*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Neural Status")
            gr.Textbox(label="Active Persona", value=SYSTEM_PROMPT, interactive=False)
            mode = gr.Radio(["Curator (12B - Fast)", "Devourer (27B - Deep)"], label="Operating Mode", value="Curator (12B - Fast)")
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Secure Workspace")
            msg = gr.Textbox(label="Input Command", placeholder="Type 'Execute' or ask a clinical question...")
            
            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Context")

    msg.submit(chat_logic, [msg, chatbot], [chatbot])
    submit.click(chat_logic, [msg, chatbot], [chatbot])

if __name__ == "__main__":
    print("Launching Jules Web Interface...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
"""
}

# --- BUILDER LOGIC ---
def build_jules():
    print("Initializing Jules v2 (Web Enabled)...")
    for directory in DIRS:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✔ Created: {directory}")
        except Exception as e: pass

    for path, content in FILES.items():
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"✔ Generated: {path}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n✅ BUILD COMPLETE.")
    print(f"1. cd {PROJECT_NAME}")
    print("2. pip install -r requirements.txt")
    print("3. python web_ui.py")

if __name__ == "__main__":
    build_jules()
