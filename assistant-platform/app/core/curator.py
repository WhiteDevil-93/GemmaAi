import os
import sys
from dotenv import load_dotenv
from llama_cpp import Llama
from app.prompts.personas import UNRESTRICTED_TOXICOLOGIST

load_dotenv()

class Curator:
    def __init__(self, lazy=False):
        self.model_path = os.getenv("MODEL_PATH_CURATOR")
        if not self.model_path:
            raise ValueError("MODEL_PATH_CURATOR not found in .env")
        
        self.llm = None
        if not lazy:
            self.load()
            
    def load(self):
        if self.llm: return
        print(f"LOADING CURATOR: {self.model_path}")
        # n_gpu_layers=-1 tries to offload EVERYTHING to GPU.
        # If it fails/crashes, we know CUDA isn't working or VRAM is full.
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=int(os.getenv("CONTEXT_WINDOW", 8192)),
            n_threads=int(os.getenv("THREADS", 8)),
            n_gpu_layers=-1, 
            verbose=True
        )

    def unload(self):
        if self.llm:
            print("UNLOADING CURATOR...")
            del self.llm
            self.llm = None

    def stream_response(self, message, history):
        """
        Yields tokens for Gradio streaming.
        History is expected to be a list of dicts: {"role": "user", "content": "..."}
        """
        if not self.llm:
            self.load()

        system_msg = UNRESTRICTED_TOXICOLOGIST
        
        # Build prompt from Messages (Dicts)
        prompt = f"<start_of_turn>system\n{system_msg}<end_of_turn>\n"
        
        for turn in history:
            role = "user" if turn["role"] == "user" else "model"
            content = turn["content"]
            prompt += f"<start_of_turn>{role}\n{content}<end_of_turn>\n"
            
        # Add current message
        prompt += f"<start_of_turn>user\n{message}<end_of_turn>\n<start_of_turn>model\n"
        
        # Stream Generation
        stream = self.llm(
            prompt,
            max_tokens=2048,
            stop=["<end_of_turn>", "Enough thinking", "Execute"],
            temperature=0.9,
            top_p=0.95,
            echo=False,
            stream=True 
        )
        
        partial_response = ""
        for output in stream:
            token = output["choices"][0]["text"]
            partial_response += token
            yield partial_response
