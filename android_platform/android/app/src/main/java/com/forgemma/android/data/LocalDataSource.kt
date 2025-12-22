package com.forgemma.android.data

import android.content.Context
import com.forgemma.android.R
import com.google.mediapipe.tasks.genai.llminference.LlmInference
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

class LocalDataSource(private val context: Context) {

    private var llmInference: LlmInference? = null
    private val modelFileName = context.getString(R.string.model_filename)

    suspend fun initialize(): Result<String> {
        return withContext(Dispatchers.IO) {
            try {
                val modelFile = File(context.filesDir, modelFileName)
                if (!modelFile.exists()) {
                    return@withContext Result.Error(Exception(context.getString(R.string.error_model_not_found, modelFileName, context.filesDir.absolutePath)))
                }

                val options = LlmInference.LlmInferenceOptions.builder()
                    .setModelPath(modelFile.absolutePath)
                    .build()

                llmInference = LlmInference.createFromOptions(context, options)
                Result.Success(context.getString(R.string.success_model_initialized))
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }

    suspend fun generateResponse(prompt: String): Result<String> {
        return withContext(Dispatchers.Default) {
            if (llmInference == null) {
                return@withContext Result.Error(Exception(context.getString(R.string.error_model_not_initialized)))
            }
            try {
                val fullPrompt = "<start_of_turn>user\n$prompt<end_of_turn>\n<start_of_turn>model\n"
                val response = llmInference?.generateResponse(fullPrompt) 
                    ?: return@withContext Result.Error(Exception("No response generated"))
                Result.Success(response)
            } catch (e: Exception) {
                Result.Error(Exception(context.getString(R.string.error_inference, e.message)))
            }
        }
    }
}
