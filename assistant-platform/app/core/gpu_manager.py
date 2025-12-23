import gc
import torch # Useful for CUDA cache clearing

class GPUManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPUManager, cls).__new__(cls)
            cls._instance.active_model_id = None
            cls._instance.registry = {} # Stores {model_id: model_object}
        return cls._instance

    def register(self, model_id, model_obj):
        """Registers a model object that must have load() and unload() methods."""
        self.registry[model_id] = model_obj
        print(f">> GPU_MANAGER: Registered {model_id}")

    def request_model(self, model_id):
        """Swaps the requested model into VRAM, unloading the previous one."""
        if self.active_model_id == model_id:
            return True # Already loaded
            
        print(f">> GPU_MANAGER: Swap requested for [{model_id}]...")
        
        # 1. Unload current model
        if self.active_model_id in self.registry:
            print(f">> GPU_MANAGER: Unloading {self.active_model_id}")
            self.registry[self.active_model_id].unload()
            self.active_model_id = None
            # Explicit GC
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        # 2. Load requested model
        if model_id in self.registry:
            print(f">> GPU_MANAGER: Loading {model_id}")
            try:
                self.registry[model_id].load()
                self.active_model_id = model_id
                return True
            except Exception as e:
                print(f">> GPU_MANAGER ERROR: Failed to load {model_id}: {e}")
                return False
        else:
            print(f">> GPU_MANAGER ERROR: Model id {model_id} not registered.")
            return False

    def get_active(self):
        return self.active_model_id
