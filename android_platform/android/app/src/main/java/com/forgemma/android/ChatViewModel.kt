package com.forgemma.android

import android.app.Application
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.forgemma.android.data.ChatRepositoryImpl
import com.forgemma.android.data.LocalDataSource
import com.forgemma.android.data.RemoteDataSource
import com.forgemma.android.data.Result
import kotlinx.coroutines.launch

data class ChatMessage(val content: String, val isUser: Boolean)

class ChatViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = ChatRepositoryImpl(
        LocalDataSource(application),
        RemoteDataSource(application),
        application
    )
    
    // UI State
    val messages = mutableStateListOf<ChatMessage>()
    val status = mutableStateOf(application.getString(R.string.status_initializing))
    
    // Toggles
    val useCloudKnowledge = mutableStateOf(false)

    init {
        viewModelScope.launch {
            when (val result = repository.initialize()) {
                is Result.Success -> {
                    status.value = result.data
                    messages.add(ChatMessage("System: ${result.data}", false))
                }
                is Result.Error -> {
                    status.value = "Error: ${result.exception.message}"
                }
                Result.Loading -> status.value = getApplication<Application>().getString(R.string.status_initializing)
            }
        }
    }

    fun sendMessage(text: String) {
        if (text.isBlank()) return

        // Add user message
        messages.add(ChatMessage(text, true))

        viewModelScope.launch {
            // Update status based on mode
            status.value = if (useCloudKnowledge.value) 
                getApplication<Application>().getString(R.string.status_consulting_cloud)
            else 
                getApplication<Application>().getString(R.string.status_thinking_local)

            when (val result = repository.sendMessage(text, useCloudKnowledge.value)) {
                is Result.Success -> {
                    messages.add(ChatMessage(result.data, false))
                    status.value = getApplication<Application>().getString(R.string.status_ready)
                }
                is Result.Error -> {
                    messages.add(ChatMessage("Error: ${result.exception.message}", false))
                    status.value = "Error encountered"
                }
                Result.Loading -> {}
            }
        }
    }
}
