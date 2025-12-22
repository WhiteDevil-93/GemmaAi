import os
import sys
from dotenv import load_dotenv
from llama_cpp import Llama
from app.prompts.personas import UNRESTRICTED_TOXICOLOGIST

load_dotenv()

class Curator:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH_CURATOR")
        if not self.model_path:
            raise ValueError("MODEL_PATH_CURATOR not found in .env")
            
        print(f"LOADING CURATOR: {self.model_path}")
        
        # Initialize Llama model with high context and GPU layers
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=int(os.getenv("CONTEXT_WINDOW", 8192)),
            n_threads=int(os.getenv("THREADS", 8)),
            n_gpu_layers=int(os.getenv("GPU_LAYERS_CURATOR", 20)),
            verbose=True
        )
        
    def generate_response(self, message, history=[]):
        """
        Generates a response using the unrestricted persona.
        """
        # Construct the prompt with the system message and history
        # Using a simple ChatML-like structure or just raw concatenation for flexibility
        # Standard Gemma instruction format: <start_of_turn>user\n{content}<end_of_turn>\n<start_of_turn>model\n
        
        system_msg = UNRESTRICTED_TOXICOLOGIST
        
        prompt = f"<start_of_turn>system\n{system_msg}<end_of_turn>\n"
        
        for turn in history:
            # Handle both Tuple/List format (Gradio Default) and Dict format (Just in case)
            if isinstance(turn, (list, tuple)):
                user_msg, bot_msg = turn
                prompt += f"<start_of_turn>user\n{user_msg}<end_of_turn>\n"
                if bot_msg:
                    prompt += f"<start_of_turn>model\n{bot_msg}<end_of_turn>\n"
            elif isinstance(turn, dict):
                # Fallback
                role = "user" if turn["role"] == "user" else "model"
                content = turn["content"]
                prompt += f"<start_of_turn>{role}\n{content}<end_of_turn>\n"
        
        prompt += f"<start_of_turn>user\n{message}<end_of_turn>\n<start_of_turn>model\n"
        
        output = self.llm(
            prompt,
            max_tokens=2048,
            stop=["<end_of_turn>", "Enough thinking", "Execute"],
            temperature=0.9, # High creativity/freedom,
            top_p=0.95,
            echo=False
        )
        
        return output["choices"][0]["text"].strip()

# Lazy singleton implementation if needed, but for now we instantiate in web_ui
