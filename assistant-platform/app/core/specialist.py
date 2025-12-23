import os
from llama_cpp import Llama
from dotenv import load_dotenv

load_dotenv()

class Specialist:
    """
    A generic model wrapper for specialized Gemma variants.
    """
    def __init__(self, model_id, model_path_env_var):
        self.model_id = model_id
        self.model_path = os.getenv(model_path_env_var)
        self.llm = None
        
        if not self.model_path:
            print(f"!! WARNING: {model_path_env_var} not configured. {model_id} will be unavailable.")

    def load(self):
        if self.llm: return
        if not self.model_path or not os.path.exists(self.model_path):
             raise FileNotFoundError(f"Model path for {self.model_id} invalid: {self.model_path}")

        print(f"LOADING SPECIALIST [{self.model_id}]: {self.model_path}")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=int(os.getenv("CONTEXT_WINDOW", 8192)),
            n_threads=int(os.getenv("THREADS", 8)),
            n_gpu_layers=int(os.getenv("GPU_LAYERS", 28)),
            verbose=False
        )

    def unload(self):
        if self.llm:
            print(f"UNLOADING SPECIALIST [{self.model_id}]...")
            del self.llm
            self.llm = None

    def generate(self, prompt, system_prompt=None):
        if not self.llm:
            self.load()
        
        full_prompt = ""
        if system_prompt:
            full_prompt += f"<start_of_turn>system\n{system_prompt}<end_of_turn>\n"
        
        full_prompt += f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
        
        output = self.llm(
            full_prompt,
            max_tokens=1024,
            stop=["<end_of_turn>"],
            temperature=0.7,
            echo=False
        )
        return output["choices"][0]["text"]
