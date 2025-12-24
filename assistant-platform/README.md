# Assistant Platform

This project implements an assistant platform with a modular architecture.

## Architecture Overview

### Application Layer (`app/`)
*   **`core/`**: The Curator (Gemma 12B logic).
*   **`tools/`**: The Execution Layer (The Devourer logic).
*   **`prompts/`**: "Toxicologist" System Prompts.
*   **`schemas/`**: JSON definitions for strict governance.
*   **`connectors/`**: Bridges to external services (Discord/OBS).

### Data Layer (`data/`)
*   **`input/`**: Data sets input directory.
*   **`output/`**: The Audit Trail (Versioned outputs).
*   **`vectors/`**: The Index (Vector storage for The Devourer).

### Documentation & Tests
*   **`docs/`**: Project documentation.
*   **`tests/`**: Test suite.

## Configuration

1. Copy the `.env.template` file to `.env`:
   ```bash
   cp .env.template .env
   ```
2. Ensure you have the model file `gemma-2b-it-gpu-int4.bin` (or your chosen model) in the root of the `assistant-platform` directory or update the paths in `.env`.
   - Update `MODEL_PATH_CURATOR` and `MODEL_PATH_DEVOURER` variables in `.env` to match your filename/path.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage

Run the web interface:
```bash
python web_ui.py
```

This will launch the Gradio interface, accessible at `http://localhost:7860`.
