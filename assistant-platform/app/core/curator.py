from app.core.gpu_manager import GPUManager

load_dotenv()

class Curator:
    def __init__(self, lazy=False):
        self.model_path = os.getenv("MODEL_PATH_CURATOR")
        if not self.model_path:
            raise ValueError("MODEL_PATH_CURATOR not found in .env")
        
        self.llm = None
        self.gpu_manager = GPUManager()
        self.gpu_manager.register("curator", self)
        
        if not lazy:
            self.gpu_manager.request_model("curator")
            
    def load(self):
        if self.llm: return
        print(f"LOADING CURATOR: {self.model_path}")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=int(os.getenv("CONTEXT_WINDOW", 8192)),
            n_threads=int(os.getenv("THREADS", 8)),
            n_gpu_layers=int(os.getenv("GPU_LAYERS", 28)), 
            verbose=True
        )

    def unload(self):
        if self.llm:
            print("UNLOADING CURATOR...")
            del self.llm
            self.llm = None

    def stream_response(self, message, history):
        # Ensure we are in VRAM
        self.gpu_manager.request_model("curator")

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
