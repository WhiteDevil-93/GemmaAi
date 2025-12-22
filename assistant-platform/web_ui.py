import gradio as gr
import os
import sys
import threading
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.curator import Curator
from app.tools.devourer import Devourer
from app.core.gpu_manager import GPUManager

load_dotenv()

# --- SYSTEMS ---
print(">> SYSTEM: INIT COMPONENTS...")
manager = GPUManager()
curator = Curator(lazy=True) # Don't load yet
devourer = Devourer(lazy=True)

manager.register(curator, devourer)

# Start with Curator
manager.request_curator()

# --- LOGIC ---
def chat_logic(message, history):
    """
    Generator function for Streaming.
    History is a list of dicts: [{'role': 'user', 'content': '...'}, ...]
    """
    # 1. Add User Message
    history.append({"role": "user", "content": message})
    # Ensure response follows 'UNRESTRICTED_TOXICOLOGIST' persona (Julia)
    yield "", history

    # 2. Check Triggers
    if "index data" in message.lower() or "ingest" in message.lower():
         threading.Thread(target=run_ingestion).start()
         history.append({"role": "assistant", "content": "Initializing Background Ingestion Protocol..."})
         yield "", history
         return

    # 3. Ensure Curator is Active (Swap if needed)
    manager.request_curator()

    # 4. Stream Response
    try:
        # Prepare history for the model (everything except the last item which is the new prompt)
        # Actually curator.stream_response takes (message, history_context)
        # We pass the full history because we want it to know context.
        # But we need an empty "assistant" block to fill.
        
        history.append({"role": "assistant", "content": ""})
        
        # Stream
        # Note: We pass history[:-2] (context) and message (current) to generator?
        # Let's just pass `message` and `history` (excluding the empty assistant block we just added)
        
        generator = curator.stream_response(message, history[:-2]) 
        
        for partial_text in generator:
            history[-1]["content"] = partial_text
            yield "", history
            
    except Exception as e:
        history[-1]["content"] = f"[ERROR]: {e}"
        yield "", history

def run_ingestion():
    """Background task wrapper"""
    # Swap to Devourer
    manager.request_devourer()
    print(">> JOB: Starting Data Ingestion...")
    result = devourer.ingest_data()
    print(f">> JOB: {result}")
    # Determine if we swap back? Maybe wait for user interaction.
    # Manager handles lazy swapping on next chat_logic call.

# --- UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🏥 Julia: Clinical AI Operations")
    
    with gr.Row():
        with gr.Column(scale=1):
            status_box = gr.Textbox(label="System Status", value="ACTIVE", interactive=False)
            sync_btn = gr.Button("🔄 Ingest Data (Local + Mobile)")
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Secure Workspace", type="messages")
            msg = gr.Textbox(label="Input Command", placeholder="Type 'Execute'...")
            
            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Context")

    # Wire up Event Handlers
    # Using submit/click with `concurrency_limit` for streaming safety if needed
    msg.submit(chat_logic, [msg, chatbot], [msg, chatbot])
    submit.click(chat_logic, [msg, chatbot], [msg, chatbot])
    
    # Sync
    sync_btn.click(fn=run_ingestion, inputs=None, outputs=None) 

if __name__ == "__main__":
    print("Launching Julia Web Interface (Streaming + Messages API)...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
