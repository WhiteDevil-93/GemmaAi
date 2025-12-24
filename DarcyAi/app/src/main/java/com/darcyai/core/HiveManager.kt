package com.darcyai.core

import android.util.Log

// Enum defining available specialist models
enum class ModelType(val modelName: String, val sizeBytes: Long) {
    TRAFFIC_OFFICER("function_gemma_270m.bin", 300L * 1024 * 1024),
    MAIN_ASSISTANT("gemma_3n_e4b_it.bin", 4L * 1024 * 1024 * 1024), // Approx
    SPECIALIST_CODE("code_gemma_2b.bin", 2L * 1024 * 1024 * 1024),
    SPECIALIST_MEDICAL("med_gemma_4b.bin", 4L * 1024 * 1024 * 1024)
}

// Conceptual interface for the LiteRT wrapper
interface LiteRTModel {
    fun generate(prompt: String): String
    fun close()
}

/**
 * HiveManager manages the lifecycle of AI models on the Edge.
 * It ensures only one specialist runs at a time to stay within the 12GB RAM budget.
 * It explicitly targets the NPU.
 */
class HiveManager {

    private var currentModel: LiteRTModel? = null
    private var currentModelType: ModelType? = null

    companion object {
        const val TAG = "HiveManager"
        const val TARGET_DEVICE = "NPU" // Explicitly target Snapdragon 8 Elite NPU
    }

    /**
     * Routes the user intent. First checks with Traffic Officer (if not loaded),
     * then loads the appropriate specialist.
     */
    suspend fun processRequest(prompt: String): String {
        // 1. Load Traffic Officer to classify
        // Optimization: In a real app, Traffic Officer might be kept resident if small enough.
        // For strict memory safety, we treat it as a swappable unit here or assume it's small.

        // Simulating intent classification
        val intent = classifyIntent(prompt)

        val requiredModel = when(intent) {
            "CODE" -> ModelType.SPECIALIST_CODE
            "MEDICAL" -> ModelType.SPECIALIST_MEDICAL
            else -> ModelType.MAIN_ASSISTANT
        }

        if (currentModelType != requiredModel) {
            loadModel(requiredModel)
        }

        return currentModel?.generate(prompt) ?: "Error: Model not loaded"
    }

    private fun classifyIntent(prompt: String): String {
        // In reality, this would run the TrafficOfficer model.
        // Heuristic simulation:
        if (prompt.contains("function") || prompt.contains("code") || prompt.contains("class")) return "CODE"
        if (prompt.contains("symptom") || prompt.contains("diagnosis")) return "MEDICAL"
        return "GENERAL"
    }

    private fun loadModel(type: ModelType) {
        Log.i(TAG, "Switching from $currentModelType to $type")

        // CRITICAL: Close previous model to free NPU/RAM resources
        currentModel?.close()
        currentModel = null
        System.gc() // Suggest GC

        // Initialize new model
        // This is where we would call the Google AI Edge SDK / LiteRT API
        // val options = LiteRtOptions.builder().setAccelerator(Accelerator.NPU).build()
        // currentModel = LiteRtModel.load(type.modelName, options)

        currentModel = MockLiteRTModel(type.modelName)
        currentModelType = type
        Log.i(TAG, "Loaded $type on $TARGET_DEVICE")
    }

    fun forceStop() {
        currentModel?.close()
        currentModel = null
        currentModelType = null
        Log.i(TAG, "HiveManager stopped. NPU resources freed.")
    }
}

class MockLiteRTModel(private val name: String) : LiteRTModel {
    override fun generate(prompt: String): String {
        return "[$name on NPU]: Processed '$prompt' efficiently."
    }

    override fun close() {
        Log.d("LiteRT", "Closed model $name")
    }
}
