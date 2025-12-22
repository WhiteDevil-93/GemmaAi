package com.forgemma.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.forgemma.android.ui.theme.ForGemmaTheme

class MainActivity : ComponentActivity() {
    private val viewModel by viewModels<ChatViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ForGemmaTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    ChatScreen(viewModel)
                }
            }
        }
    }
}

@Composable
fun ChatScreen(viewModel: ChatViewModel) {
    var inputText by remember { mutableStateOf("") }
    val messages = viewModel.messages
    val status by viewModel.status
    var useCloud by viewModel.useCloudKnowledge

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        // Header / Status
        Text(
            text = androidx.compose.ui.res.stringResource(R.string.header_title),
            style = MaterialTheme.typography.headlineSmall
        )
        Text(
            text = androidx.compose.ui.res.stringResource(R.string.status_label) + status,
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray
        )
        
        // Settings Row
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(vertical = 8.dp)
        ) {
            Text(androidx.compose.ui.res.stringResource(R.string.toggle_cloud_label))
            Spacer(Modifier.width(8.dp))
            Switch(
                checked = useCloud,
                onCheckedChange = { useCloud = it }
            )
        }

        Divider()

        // Chat List
        LazyColumn(
            modifier = Modifier.weight(1f).padding(vertical = 8.dp),
            reverseLayout = false
        ) {
            items(messages) { message ->
                MessageBubble(message)
            }
        }

        // Input Area
        Row(
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextField(
                value = inputText,
                onValueChange = { inputText = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text(androidx.compose.ui.res.stringResource(R.string.input_placeholder)) }
            )
            Spacer(Modifier.width(8.dp))
            Button(
                onClick = {
                    viewModel.sendMessage(inputText)
                    inputText = ""
                }
            ) {
                Text(androidx.compose.ui.res.stringResource(R.string.btn_send))
            }
        }
    }
}

@Composable
fun MessageBubble(message: ChatMessage) {
    val align = if (message.isUser) Alignment.End else Alignment.Start
    val color = if (message.isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = align
    ) {
        Card(
            modifier = Modifier.padding(4.dp).widthIn(max = 300.dp),
            colors = CardDefaults.cardColors(containerColor = color)
        ) {
            Text(
                text = message.content,
                modifier = Modifier.padding(8.dp)
            )
        }
    }
}
