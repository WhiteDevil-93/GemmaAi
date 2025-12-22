package com.forgemma.android.data

import com.forgemma.android.ChatMessage

interface ChatRepository {
    suspend fun initialize(): Result<String>
    suspend fun sendMessage(message: String, useCloud: Boolean): Result<String>
}
