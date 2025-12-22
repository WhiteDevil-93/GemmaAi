# ForGemma Android Framework

This project contains the framework and source code for an Android application designed to run the **Gemma 3n E4B** model locally and access a 27B knowledge base via the cloud.

## Features

- **Local Inference**: Runs Gemma 3n E4B (4 Billion parameters, optimized for edge) on-device using MediaPipe GenAI.
- **Hybrid Reasoning**: Capable of switching between local processing and a cloud-based 27B Knowledge Base.
- **Chat Interface**: Simple Jetpack Compose UI for interaction.

## Prerequisites

- **Android Studio** (Koala or later recommended)
- **Android SDK** 34
- **Physical Android Device** with reasonable RAM (8GB+ recommended for 4B model) and NPU/GPU support.

## Setup Instructions

### 1. Download Model Weights

The Gemma 3n E4B model is not included in this repo due to size.

1. Download `gemma-3n-e4b.bin` (MediaPipe/TFLite formatted) from Hugging Face or Kaggle Models.
   - Ensure the format is compatible with MediaPipe GenAI (often `.bin` or `.task`).
2. Rename the file to `gemma-3n-e4b.bin`.
3. Push the file to the app's internal storage directory on your device:

   ```bash
   adb push gemma-3n-e4b.bin /data/local/tmp/
   # Then move it to app's files dir via code or manually if rooted.
   # Easier method for development: 
   # Use Android Studio Device Explorer to upload to /data/data/com.forgemma.android/files/
   ```

   *Note: The code expects the file at `context.filesDir + "/gemma-3n-e4b.bin"`.*

### 2. Configure Remote Knowledge Base

1. Open `android/app/src/main/java/com/forgemma/android/RemoteKnowledgeBase.kt`.
2. Update `BASE_URL` with the actual endpoint of your hosted 27B model (e.g., vLLM, TGI, or OpenAI-compatible API).

### 3. Build and Run

1. Open the `android` folder in Android Studio.
2. Sync Project with Gradle Files.
3. Connect your Android device.
4. Run `app`.

## Architecture

- `ChatRepository`: Interface defining the contract for data operations.
- `LocalDataSource`: Manages local inference using MediaPipe GenAI.
- `RemoteDataSource`: Handles network calls to the external API via Retrofit.
- `ChatViewModel`: Manages UI state and orchestrates data flow via the Repository.
