package com.forgemma.android.data

import android.content.Context
import com.forgemma.android.R

class ChatRepositoryImpl(
    private val localDataSource: LocalDataSource,
    private val remoteDataSource: RemoteDataSource,
    private val context: Context
) : ChatRepository {

    override suspend fun initialize(): Result<String> {
        return localDataSource.initialize()
    }

    override suspend fun sendMessage(message: String, useCloud: Boolean): Result<String> {
        return if (useCloud) {
            remoteDataSource.query(message)
        } else {
            val logicPrompt = context.getString(R.string.prompt_reasoning_template, message)
            localDataSource.generateResponse(logicPrompt)
        }
    }
}
