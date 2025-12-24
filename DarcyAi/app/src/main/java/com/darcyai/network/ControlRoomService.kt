package com.darcyai.network

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

// Data classes for exchange
data class CommandRequest(
    val command: String,
    val source: String = "DarcyAi_Mobile",
    val timestamp: Long = System.currentTimeMillis()
)

data class CommandResponse(
    val status: String,
    val result: String,
    val agent: String // "Julia" or "Athena"
)

data class SyncData(
    val governanceRules: String,
    val schemas: List<String>
)

// Retrofit Interface for Control Room (Laptop)
interface ControlRoomService {

    @POST("/api/command")
    suspend fun sendCommand(@Body request: CommandRequest): CommandResponse

    @GET("/api/sync")
    suspend fun syncGovernance(): SyncData

    @GET("/api/health")
    suspend fun checkHealth(): String
}

object NetworkClient {
    // Placeholder base URL - in production, this would be the local IP of the Control Room laptop
    const val BASE_URL = "http://192.168.1.100:8000/"
}
