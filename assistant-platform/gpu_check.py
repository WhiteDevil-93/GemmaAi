from llama_cpp import Llama
import os
from dotenv import load_dotenv

load_dotenv("assistant-platform/.env") # Explicit path for now

import sys
# Add NVIDIA DLLs to PATH for llama-cpp-python
def setup_nvidia_paths():
    base_path = os.path.dirname(sys.executable) # scripts
    site_packages = os.path.join(os.path.dirname(base_path), 'Lib', 'site-packages')
    
    nvidia_libs = [
        os.path.join(site_packages, 'nvidia', 'cuda_runtime', 'bin'),
        os.path.join(site_packages, 'nvidia', 'cublas', 'bin'),
    ]
    
    for path in nvidia_libs:
        if os.path.exists(path):
            try:
                os.add_dll_directory(path) # For Python 3.8+ DLL loading
            except:
                pass
            os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
            print(f"Added DLL path: {path}")

setup_nvidia_paths()

print("--- GPU DIAGNOSIS ---")
try:
    import llama_cpp
    print(f"Lib location: {llama_cpp.__file__}")

    # Attempt to load a dummy model or just check internal flags if possible
    # But easiest is to try loading one of our existing models with verbose logging
    default_path = "C:/Users/anon3/GemmaAi/assistant-platform/models/gemma-3-12b-it-uncensored.Q5_K_M.gguf"
    model_path = os.getenv("MODEL_PATH_CURATOR", default_path)
    
    print(f"Loading: {model_path}")
    if not os.path.exists(model_path):
        print(f"CRITICAL: Model file not found at {model_path}")
    
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1, # Request ALL layers
        verbose=True
    )
    
    print(f"Metadata: {llm.metadata}")
    print("Check the logs above for 'BLAS = 1' or 'CUDA = 1'. If it says 'BLAS = 0', you are on CPU.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
