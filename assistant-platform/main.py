import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style

load_dotenv()
init()

def main():
    print(f"{Fore.CYAN}[JULIA]{Style.RESET_ALL} Control Room CLI Active.")
    print("Run 'python web_ui.py' to launch the visual interface.")

if __name__ == "__main__":
    main()