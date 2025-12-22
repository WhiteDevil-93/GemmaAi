import sys
import torch
import platform

def system_check():
    print("========================================")
    print("   FORGEMMA: SYSTEM DIAGNOSTIC TOOL     ")
    print("========================================")
    
    # Check Python Environment
    print(f"[+] Python Version: {sys.version.split()[0]}")
    print(f"[+] OS: {platform.system()} {platform.release()}")

    # Check for GPU Availability
    if torch.cuda.is_available():
        print(f"[+] GPU Detected: {torch.cuda.get_device_name(0)}")
        print(f"[+] VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(">> STATUS: READY FOR ACCELERATED INFERENCE.")
    else:
        print("[-] GPU Not Detected.")
        print(">> STATUS: RUNNING ON CPU (Performance will be limited).")

def main():
    system_check()
    print("\n----------------------------------------")
    print("Framework initialized successfully.")
    print("Waiting for Gemma model weights...")
    print("----------------------------------------")

if __name__ == "__main__":
    main()
