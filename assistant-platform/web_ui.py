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
        # Compatibility: History is list of [user_msg, bot_msg] lists/tuples
        history.append([message, "[FATAL]: Curator corrupted."])
        return "", history
    
    # Check for User Commands
    if "index onedrive" in message.lower() or "sync data" in message.lower():
        threading.Thread(target=run_ingestion).start()
        history.append([message, "[JULES]: Background Indexing Initiated."])
        return "", history

    try:
        # We need to construct the prompt from the history of [user, bot] pairs
        # The Curator checks for dicts currently, we need to fix that too or convert here.
        # Let's fix Curator to handle the tuples again because Gradio 4 passes tuples by default for Chatbot without type="messages".
        
        # ACTUALLY: Let's keep Curator robust. 
        # But for NOW, let's just make the UI work with the default Tuple format.
        
        # 1. Generate Response
        # We pass the history as-is (list of lists/tuples).
        # We need to modify Curator to handle this format again.
        response = curator.generate_response(message, history)
        
        # 2. Append result
        history.append([message, response])
        
        return "", history
    except Exception as e:
        history.append([message, f"[ERROR]: {e}"])
        return "", history

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
    # Wire up Event Handlers
    # Note: chat_logic returns (empty_string, new_history).
    # so we map outputs to [msg, chatbot] to clear the box and update the chat.
    msg.submit(chat_logic, [msg, chatbot], [msg, chatbot])
    submit.click(chat_logic, [msg, chatbot], [msg, chatbot])
    
    # Sync Button
    sync_btn.click(fn=run_ingestion, inputs=None, outputs=None) 
    # Note: Gradio output for background threads is tricky without streaming, 
    # for now we rely on the console logs or the Curator knowing it happened.

if __name__ == "__main__":
    print("Launching Jules Web Interface (Curator-Driven)...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
