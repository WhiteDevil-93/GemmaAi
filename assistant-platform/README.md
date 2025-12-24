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
2. Ensure you have the model file `gemma-3n-E4B-it-int4.bin` in the root of the `assistant-platform` directory.
   - If your model file has a different name, update the `MODEL_PATH_CURATOR` and `MODEL_PATH_DEVOURER` variables in `.env` to match your filename.
