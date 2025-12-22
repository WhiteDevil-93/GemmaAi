import gc
import torch # Just for VRAM clearing if needed (though llama-cpp handles its own)
# Actually, llama-cpp-python manages its own memory context.
# We just need to nullify the references.

class GPUManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPUManager, cls).__new__(cls)
            cls._instance.active_model = None
            cls._instance.curator_ref = None
            cls._instance.devourer_ref = None
        return cls._instance

    def register(self, curator, devourer):
        self.curator_ref = curator
        self.devourer_ref = devourer

    def request_curator(self):
        if self.active_model == "curator":
            return
            
        print(">> GPU_MANAGER: Swapping to CURATOR...")
        if self.devourer_ref:
            self.devourer_ref.unload()
        
        if self.curator_ref:
            self.curator_ref.load()
            
        self.active_model = "curator"

    def request_devourer(self):
        if self.active_model == "devourer":
            return
            
        print(">> GPU_MANAGER: Swapping to DEVOURER...")
        if self.curator_ref:
            self.curator_ref.unload()
            
        if self.devourer_ref:
            self.devourer_ref.load()
            
        self.active_model = "devourer"
