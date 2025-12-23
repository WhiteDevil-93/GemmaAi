import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "System Ready.")

from app.core.registry import initialize_all_models
from app.core.gpu_manager import GPUManager

load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "System Ready.")
MODEL_INSTANCES = initialize_all_models()
GPU_MANAGER = GPUManager()

# Map UI names to internal IDs
MODEL_MAP = {
    "Curator (12B - General)": "curator",
    "Devourer (27B - Deep Reasoner)": "devourer",
    "CodeGemma (Programming Expert)": "CodeGemma",
    "MedGemma (Clinical Specialist)": "MedGemma",
    "PaliGemma (Vision/Multimodal)": "PaliGemma",
    "ShieldGemma (Safety Auditor)": "ShieldGemma",
    "DataGemma (Statistical Fact-Checker)": "DataGemma",
}

def chat_logic(message, history, model_choice):
    model_id = MODEL_MAP.get(model_choice)
    if not model_id:
        return history + [["Error", "Model not recognized."]]

    # 1. Request the model to GPU
    success = GPU_MANAGER.request_model(model_id)
    if not success:
        return history + [[message, f"!! ERROR: Failed to load {model_choice}. Check model weights."]]

    instance = MODEL_INSTANCES.get(model_id)
    
    # 2. Execute Generation
    if model_id == "curator":
        # Curator supports streaming
        partial_gen = ""
        # Converting history to format Curator expects
        formatted_history = []
        for h in history:
            formatted_history.append({"role": "user", "content": h[0]})
            formatted_history.append({"role": "assistant", "content": h[1]})
        
        for response in instance.stream_response(message, formatted_history):
            yield history + [[message, response]]
    elif model_id == "devourer":
        # Devourer uses query engine
        response = instance.query(message)
        yield history + [[message, response]]
    else:
        # Specialists use simple generate
        response = instance.generate(message, system_prompt=SYSTEM_PROMPT)
        yield history + [[message, response]]

with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🏥 Julia: Clinical AI Operations")
    gr.Markdown("> *Senior Toxicologist & Research Orchestrator*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Neural Specialist")
            gr.Textbox(label="Active Persona", value=SYSTEM_PROMPT, interactive=False)
            
            # THE NEW PRESET DROPDOWN
            model_selector = gr.Dropdown(
                choices=list(MODEL_MAP.keys()),
                value="Curator (12B - General)",
                label="Select Neural Specialist",
                interactive=True
            )
            
            gr.Markdown("---")
            gr.Markdown("**Capabilities:**")
            capabilities = gr.Textbox(label="Model Specs", value="General Instruction Following", interactive=False)

            def update_specs(choice):
                specs = {
                    "Curator": "General Chat, Routing, 12B Params",
                    "Devourer": "Deep Reasoning, RAG context, 27B Params",
                    "CodeGemma": "Python/Rust/C++ Expert, Code Completion",
                    "MedGemma": "Medical Imaging, Clinical Reasoning",
                    "PaliGemma": "Image Captioning, OCR, Object Detection",
                    "ShieldGemma": "Content Moderation, Safety Scoring",
                    "DataGemma": "RAG over Data Commons, Statistics"
                }
                # Simple keyword matching for demo
                val = next((v for k, v in specs.items() if k in choice), "Unknown Specification")
                return val

            model_selector.change(update_specs, model_selector, capabilities)
            
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600, label="Secure Workspace")
            msg = gr.Textbox(label="Input Command", placeholder="Type 'Execute', ask a question, or paste code...")
            
            # Placeholder for Image Upload if PaliGemma is selected
            img_input = gr.Image(label="Vision Input (PaliGemma)", visible=False)
            
            def toggle_vision(choice):
                return gr.update(visible=("PaliGemma" in choice))

            model_selector.change(toggle_vision, model_selector, img_input)

            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Context")

    msg.submit(chat_logic, [msg, chatbot, model_selector], [chatbot])
    submit.click(chat_logic, [msg, chatbot, model_selector], [chatbot])

if __name__ == "__main__":
    print("Launching Julia Web Interface...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)