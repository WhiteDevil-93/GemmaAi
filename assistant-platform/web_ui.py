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