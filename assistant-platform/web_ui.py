import gradio as gr
import os
import sys
import threading
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.curator import Curator
from app.tools.devourer import Devourer
from app.prompts.personas import UNRESTRICTED_TOXICOLOGIST

load_dotenv()

# --- SYSTEMS ---
print(">> SYSTEM: BOOTING CURATOR (FOREGROUND)...")
try:
    curator = Curator()
    STATUS_CURATOR = "ONLINE (12B)"
except Exception as e:
    curator = None
    STATUS_CURATOR = f"OFFLINE: {e}"

print(">> SYSTEM: BOOTING DEVOURER (BACKGROUND CPU)...")
try:
    # Devourer loads on CPU/RAM, shouldn't crash VRAM
    devourer = Devourer()
    STATUS_DEVOURER = "ONLINE (27B/CPU)"
except Exception as e:
    devourer = None
    STATUS_DEVOURER = f"OFFLINE: {e}"

# --- LOGIC ---
def chat_logic(message, history):
    if not curator:
        return "[FATAL]: Curator corrupted."
    
    # Check for User Commands
    if "index onedrive" in message.lower() or "sync data" in message.lower():
        # Clean trigger manually for now, or just let the curator handle the response
        threading.Thread(target=run_ingestion).start()
        return "[JULES]: Background Indexing Initiated. Proceeding with standard protocols."

    try:
        # Standard Curator Response
        response = curator.generate_response(message, history)
        return response
    except Exception as e:
        return f"[ERROR]: {e}"

def run_ingestion():
    """Background task wrapper"""
    if devourer:
        print(">> JOB: Starting Data Ingestion...")
        result = devourer.ingest_data()
        print(f">> JOB: {result}")

def get_status():
    return f"CURATOR: {STATUS_CURATOR} | DEVOURER: {STATUS_DEVOURER}"

# --- UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🏥 Jules: Clinical AI Operations")
    gr.Markdown("> *Senior Toxicologist & Research Orchestrator*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 System Status")
            status_box = gr.Textbox(label="Diagnostics", value=get_status(), interactive=False, lines=2)
            sync_btn = gr.Button("🔄 Ingest Data (Local + Mobile)")
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Secure Workspace")
            msg = gr.Textbox(label="Input Command", placeholder="Type 'Execute' or ask a clinical question...")
            
            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Context")

    # Wire up Event Handlers
    msg.submit(chat_logic, [msg, chatbot], [chatbot])
    submit.click(chat_logic, [msg, chatbot], [chatbot])
    submit.click(lambda: "", None, msg)
    
    # Sync Button
    sync_btn.click(fn=run_ingestion, inputs=None, outputs=None) 
    # Note: Gradio output for background threads is tricky without streaming, 
    # for now we rely on the console logs or the Curator knowing it happened.

if __name__ == "__main__":
    print("Launching Jules Web Interface (Curator-Driven)...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
