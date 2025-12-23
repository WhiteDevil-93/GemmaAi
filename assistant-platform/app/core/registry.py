from app.core.curator import Curator
from app.tools.devourer import Devourer
from app.core.specialist import Specialist
from app.core.gpu_manager import GPUManager

def initialize_all_models():
    gpu_manager = GPUManager()
    
    # Base Models
    curator = Curator(lazy=True)
    devourer = Devourer(lazy=True)
    
    # Specialist "Girls"
    code_gemma = Specialist("CodeGemma", "MODEL_PATH_CODE")
    med_gemma = Specialist("MedGemma", "MODEL_PATH_MED")
    pali_gemma = Specialist("PaliGemma", "MODEL_PATH_VISION")
    shield_gemma = Specialist("ShieldGemma", "MODEL_PATH_SHIELD")
    data_gemma = Specialist("DataGemma", "MODEL_PATH_DATA")
    
    # Register them
    # Curator and Devourer already register themselves in __init__
    gpu_manager.register("CodeGemma", code_gemma)
    gpu_manager.register("MedGemma", med_gemma)
    gpu_manager.register("PaliGemma", pali_gemma)
    gpu_manager.register("ShieldGemma", shield_gemma)
    gpu_manager.register("DataGemma", data_gemma)
    
    return {
        "curator": curator,
        "devourer": devourer,
        "CodeGemma": code_gemma,
        "MedGemma": med_gemma,
        "PaliGemma": pali_gemma,
        "ShieldGemma": shield_gemma,
        "DataGemma": data_gemma
    }
