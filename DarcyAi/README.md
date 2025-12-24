# DarcyAi

**DarcyAi** is a specialized native Android node for a Hybrid AI Operating Platform. It is designed to run on high-end mobile hardware (specifically the Samsung S25 Ultra) to provide offline, multimodal intelligence at the edge.

## Project Objective
Scaffolded as a native Kotlin application, DarcyAi functions as a symbiotic remote for a local "Control Room" (high-capacity laptop) while capable of independent, high-speed inference.

## UI/UX: "Neural Neon"
The application follows a "Cyberpunk-Arcane" aesthetic:
- **Palette**: Deep Black backgrounds, Neon Green (#39FF14) outlines, Electric Purple/Cyan accents.
- **Components**: Star-shaped triggers, Serpentine gradients, HUD-style containers.

## Hardware Optimization
- **Target Device**: Samsung S25 Ultra (Snapdragon 8 Elite NPU).
- **Framework**: Google AI Edge SDK / LiteRT-LM.
- **Performance**: Explicitly targets `Accelerator.NPU` for >28 tokens/sec.
- **Memory**: Strict 12GB RAM budget management.

## Architecture: "The Hive"
Managed by `HiveManager`, the app uses a modular approach to model loading:
1.  **Traffic Officer**: FunctionGemma 270M (Resident/Lightweight) - Routes intent.
2.  **Main Assistant**: Gemma 3n E4B-it (Default Multimodal).
3.  **Specialists**: CodeGemma 2B, MedGemma 4B (Loaded on demand).

**Logic**: Models are dynamically loaded and unloaded (`close()`) to ensure only one heavy model occupies the NPU at a time.

## Network & Sync
- Acts as a gateway to the local "Control Room".
- Syncs governance rules and schemas from the `WhiteDevil-93/GemmaAi` repository (simulated via `ControlRoomService`).

## Setup
1.  Open in Android Studio.
2.  Ensure Android SDK 34 is installed.
3.  Place model binaries (`.bin`) in the `assets` folder (not included in repo).
4.  Build and Run on a Snapdragon 8 Gen 3/Elite device for NPU acceleration.
