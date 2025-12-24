import gradio as gr
import os
import sys
import threading
import time
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Attempt imports, fall back to mocks if necessary
try:
    from app.core.curator import Curator
    from app.tools.devourer import Devourer
    IMPORTS_SUCCESS = True
except ImportError:
    IMPORTS_SUCCESS = False
    print(">> WARNING: Core modules not found. Using Mocks.")

load_dotenv()

# --- MOCK CLASSES (For "Neural Status" Stability) ---
class MockCurator:
    def __init__(self):
        print(">> SYSTEM: Initializing Mock Curator...")
        self.model_path = "MOCK_MODEL_V1"

    def generate_response(self, message, history=[]):
        time.sleep(1) # Simulate think time
        return f"[MOCK CURATOR]: I received your message: '{message}'. The real Curator model is unavailable/offline, but I am here to ensure the UI does not crash. Please check your model paths in .env."

class MockDevourer:
    def __init__(self):
        print(">> SYSTEM: Initializing Mock Devourer...")
        self.index = "MOCK_INDEX"

    def ingest_data(self):
        time.sleep(2)
        return "✔ [MOCK] Data ingestion simulation complete."

    def query(self, message):
        return f"[MOCK DEVOURER]: I found no real documents, but here is a simulated fact about '{message}'."

# --- GLOBAL STATE ---
# We keep track of instances.
# We try to load real ones. If they fail, we use mocks.
curator_instance = None
devourer_instance = None

STATUS_CURATOR = "INITIALIZING..."
STATUS_DEVOURER = "INITIALIZING..."

def initialize_systems():
    global curator_instance, devourer_instance, STATUS_CURATOR, STATUS_DEVOURER

    # 1. Curator
    try:
        if IMPORTS_SUCCESS:
            curator_instance = Curator()
            STATUS_CURATOR = "ONLINE (12B - Real)"
        else:
            raise ImportError("Modules missing")
    except Exception as e:
        print(f"!! CURATOR LOAD FAILED: {e}")
        curator_instance = MockCurator()
        STATUS_CURATOR = "ONLINE (Simulated/Mock)"

    # 2. Devourer
    try:
        if IMPORTS_SUCCESS:
            devourer_instance = Devourer()
            STATUS_DEVOURER = "ONLINE (27B - Real)"
        else:
            raise ImportError("Modules missing")
    except Exception as e:
        print(f"!! DEVOURER LOAD FAILED: {e}")
        devourer_instance = MockDevourer()
        STATUS_DEVOURER = "ONLINE (Simulated/Mock)"

# Initialize on startup
initialize_systems()

# --- LOGIC ---
def chat_logic(message, history, model_mode):
    """
    Handles chat based on the selected 'model_mode' from the dropdown.
    """
    global curator_instance, devourer_instance
    
    if not message.strip():
        return "", history

    # Append User Message
    history.append([message, None]) # Placeholder for bot response

    response = ""

    try:
        if model_mode == "Curator (Chat)":
            if curator_instance:
                response = curator_instance.generate_response(message, history[:-1])
            else:
                response = "[SYSTEM]: Curator is not initialized."

        elif model_mode == "Devourer (RAG)":
            if devourer_instance:
                # Devourer uses a different method usually (query),
                # but we'll wrap it to look like chat or just return the query result.
                # Assuming Devourer has a .query() method based on previous file read
                response = devourer_instance.query(message)
            else:
                response = "[SYSTEM]: Devourer is not initialized."

        elif model_mode == "Debug (Mock)":
            # Force use of Mock classes logic locally
            response = f"[DEBUG MODE]: Echoing '{message}'. System Status: {get_status()}"

        else:
            response = "[SYSTEM]: Unknown Mode Selected."

    except Exception as e:
        response = f"[ERROR]: {str(e)}"

    # Update History with response
    history[-1][1] = response
    return "", history

def run_ingestion():
    global devourer_instance
    if devourer_instance:
        return devourer_instance.ingest_data()
    return "Devourer not available."

def get_status():
    return f"CURATOR: {STATUS_CURATOR} | DEVOURER: {STATUS_DEVOURER}"

# --- THEME (Cyberpunk/Neon: Cyan + Purple) ---
# Customizing the theme to match the PixAI Logo (Neon Blue/Cyan Primary, Purple/Magenta Accents, Dark Background)
theme = gr.themes.Soft(
    primary_hue="cyan",
    secondary_hue="fuchsia",
    neutral_hue="slate",
).set(
    body_background_fill="#050510", # Deep Dark Blue/Black
    body_text_color="#E0E0FF",      # Pale Blue/White text
    block_background_fill="#0F0F20", # Dark Navy Block
    block_border_color="#00FFFF",   # Neon Cyan Border
    block_title_text_color="#00FFFF", # Cyan Titles
    input_background_fill="#1A1A30",
    button_primary_background_fill="#D000FF", # Magenta/Purple Button
    button_primary_text_color="#FFFFFF",
    slider_color="#00FFFF",
)

# --- UI LAYOUT ---
with gr.Blocks(theme=theme, title="Jules: Assistant Platform") as demo:
    gr.Markdown("# 🦁 Jules: Assistant Platform")
    gr.Markdown("> *Secure AI Operations | Status: Monitoring*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚡ Neural Status")
            status_box = gr.Textbox(label="Diagnostics", value=get_status(), interactive=False, lines=2)

            # Model Selector (Multi-Model Support)
            model_selector = gr.Dropdown(
                choices=["Curator (Chat)", "Devourer (RAG)", "Debug (Mock)"],
                value="Curator (Chat)",
                label="Active Model / Persona",
                interactive=True
            )

            sync_btn = gr.Button("🔄 Ingest Data (Sync)")
            sync_output = gr.Textbox(label="Sync Status", interactive=False)
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Terminal Output")
            msg = gr.Textbox(label="Command Input", placeholder="Type 'Execute' or ask a question...")
            
            with gr.Row():
                submit = gr.Button("EXECUTE", variant="primary")
                clear = gr.Button("CLEAR CONTEXT")

    # Wire Event Handlers
    msg.submit(chat_logic, [msg, chatbot, model_selector], [msg, chatbot])
    submit.click(chat_logic, [msg, chatbot, model_selector], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)
    
    # Sync Button
    sync_btn.click(fn=run_ingestion, inputs=None, outputs=sync_output)

if __name__ == "__main__":
    print("Launching Jules Web Interface (v2.1 - Hybrid/Mock Supported)...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
