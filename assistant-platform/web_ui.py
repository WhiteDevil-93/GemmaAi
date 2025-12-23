import gradio as gr
import os
from dotenv import load_dotenv
from app.core.registry import initialize_all_models
from app.core.gpu_manager import GPUManager
from app.prompts.personas import (
    BASE_MISSION, JULIA_CORE, CRISTINA_CORE, ATHENA_CORE, 
    VESPER_CORE, LYRA_CORE, NOVA_CORE, ASTRA_CORE
)

load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "System Ready.")
MODEL_INSTANCES = initialize_all_models()
GPU_MANAGER = GPUManager()

# Map UI names to internal IDs
MODEL_MAP = {
    "Julia (12B - Lead Operations)": "curator",
    "Athena (27B - Strategic Intel)": "devourer",
    "Lyra (Systems Architect - Code)": "CodeGemma",
    "Cristina (Surgical/Clinical - Med)": "MedGemma",
    "Nova (Imaging Specialist - Vision)": "PaliGemma",
    "Vesper (Security/Integrity - Shield)": "ShieldGemma",
    "Astra (Intelligence Analyst - Data)": "DataGemma",
}

# Map internal IDs to Persona Strings
PERSONA_MAP = {
    "curator": JULIA_CORE,
    "devourer": ATHENA_CORE,
    "CodeGemma": LYRA_CORE,
    "MedGemma": CRISTINA_CORE,
    "PaliGemma": NOVA_CORE,
    "ShieldGemma": VESPER_CORE,
    "DataGemma": ASTRA_CORE,
}

def chat_logic(message, history, model_choice):
    model_id = MODEL_MAP.get(model_choice)
    if not model_id:
        yield history + [["Error", "Model not recognized."]]
        return

    # 1. Request the model to GPU
    success = GPU_MANAGER.request_model(model_id)
    if not success:
        yield history + [[message, f"!! ERROR: Failed to load {model_choice}. Check model weights."]]
        return

    instance = MODEL_INSTANCES.get(model_id)
    custom_persona = BASE_MISSION + "\n" + PERSONA_MAP.get(model_id, "")
    
    # 2. Execute Generation
    if model_id == "curator":
        formatted_history = []
        for h in history:
            formatted_history.append({"role": "user", "content": h[0]})
            formatted_history.append({"role": "assistant", "content": h[1]})
        
        for response in instance.stream_response(message, formatted_history):
            yield history + [[message, response]]
    elif model_id == "devourer":
        response = instance.query(f"Context: {custom_persona}\nRequest: {message}")
        yield history + [[message, response]]
    else:
        response = instance.generate(message, system_prompt=custom_persona)
        yield history + [[message, response]]

with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🏥 Julia: Clinical AI Operations")
    gr.Markdown("> *Senior Toxicologist & Research Orchestrator*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Neural Specialist")
            gr.Textbox(label="Active Persona", value=SYSTEM_PROMPT, interactive=False)
            
            model_selector = gr.Dropdown(
                choices=list(MODEL_MAP.keys()),
                value="Julia (12B - Lead Operations)",
                label="Select Neural Specialist",
                interactive=True
            )
            
            gr.Markdown("---")
            gr.Markdown("**Capabilities:**")
            capabilities = gr.Textbox(label="Model Specs", value="General Instruction Following", interactive=False)

            def update_specs(choice):
                specs = {
                    "Julia": "Command & Control, General Logic",
                    "Athena": "Complex Synthesis, Massive RAG contextualization",
                    "Lyra": "Protocol Automation, Code Generation & Fixes",
                    "Cristina": "Clinical Reasoning, Diagnostics, Pharmacology",
                    "Nova": "Multimodal Input, OCR, Visual Forensics",
                    "Vesper": "Policy Enforcement, Safety Guarding, Integrity Audit",
                    "Astra": "Data Commons Retrieval, Fact-based Statistics"
                }
                val = next((v for k, v in specs.items() if k in choice), "Unknown Specialist")
                return val

            model_selector.change(update_specs, model_selector, capabilities)
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Secure Workspace")
            msg = gr.Textbox(label="Input Command", placeholder="Type 'Execute', ask a question, or paste code...")
            img_input = gr.Image(label="Vision Input (PaliGemma)", visible=False)
            
            def toggle_vision(choice):
                return gr.update(visible=("Nova" in choice or "PaliGemma" in choice))

            model_selector.change(toggle_vision, model_selector, img_input)

            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Context")

    msg.submit(chat_logic, [msg, chatbot, model_selector], [chatbot])
    submit.click(chat_logic, [msg, chatbot, model_selector], [chatbot])

if __name__ == "__main__":
    print("Launching Julia Web Interface...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)