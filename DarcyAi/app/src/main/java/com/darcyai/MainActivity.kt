package com.darcyai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.darcyai.core.HiveManager
import com.darcyai.ui.components.HudHeader
import com.darcyai.ui.components.NeonContainer
import com.darcyai.ui.components.SerpentineProgressBar
import com.darcyai.ui.components.StarTrigger
import com.darcyai.ui.theme.CyanBlue
import com.darcyai.ui.theme.DarcyAiTheme
import com.darcyai.ui.theme.ElectricPurple
import com.darcyai.ui.theme.NeonGreen
import com.darcyai.ui.theme.NeuralBlack
import com.darcyai.ui.theme.TextWhite
import dev.jeziellago.compose.markdowntext.MarkdownText
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {

    private val hiveManager = HiveManager()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            DarcyAiTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = NeuralBlack
                ) {
                    MainScreen(hiveManager)
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        hiveManager.forceStop()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(hiveManager: HiveManager) {
    var input by remember { mutableStateOf("") }
    var output by remember { mutableStateOf("System Ready. Waiting for input...") }
    var isThinking by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    Column(modifier = Modifier.padding(16.dp)) {
        HudHeader("DARCY AI NODE")

        Spacer(modifier = Modifier.height(16.dp))

        // Output Display (Neural Neon HUD)
        NeonContainer(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
        ) {
            MarkdownText(
                markdown = output,
                color = TextWhite,
                style = androidx.compose.material3.MaterialTheme.typography.bodyLarge
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (isThinking) {
            SerpentineProgressBar(progress = 0.7f) // Indeterminate simulation
            Spacer(modifier = Modifier.height(8.dp))

            // Override Protocol: "Enough thinking" / "Execute"
            Button(
                onClick = {
                    isThinking = false
                    output += "\n[OVERRIDE]: Reasoning Halted. Executing immediately."
                    // hiveManager.forceStop() // Optional: kill generation
                },
                colors = ButtonDefaults.buttonColors(containerColor = ElectricPurple),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("EXECUTE NOW", color = TextWhite)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Input Area
        TextField(
            value = input,
            onValueChange = { input = it },
            modifier = Modifier.fillMaxWidth(),
            colors = TextFieldDefaults.textFieldColors(
                containerColor = NeuralBlack,
                textColor = TextWhite,
                cursorColor = NeonGreen,
                focusedIndicatorColor = NeonGreen,
                unfocusedIndicatorColor = CyanBlue
            ),
            placeholder = { Text("Enter command...", color = CyanBlue) }
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Trigger
        StarTrigger(
            text = "ENGAGE",
            onClick = {
                if (input.isNotBlank()) {
                    isThinking = true
                    output = "Thinking..."
                    scope.launch {
                        val response = hiveManager.processRequest(input)
                        output = response
                        isThinking = false
                        input = ""
                    }
                }
            },
            modifier = Modifier.align(androidx.compose.ui.Alignment.CenterHorizontally)
        )
    }
}
