package com.darcyai.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CutCornerShape
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import com.darcyai.ui.theme.CyanBlue
import com.darcyai.ui.theme.ElectricPurple
import com.darcyai.ui.theme.NeonGreen
import com.darcyai.ui.theme.NeuralBlack
import com.darcyai.ui.theme.SerpentineGreen
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun NeonContainer(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .background(NeuralBlack)
            .border(1.dp, NeonGreen, shape = CutCornerShape(topStart = 16.dp, bottomEnd = 16.dp))
            .padding(16.dp)
    ) {
        content()
    }
}

@Composable
fun StarTrigger(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .clickable(onClick = onClick)
            .padding(8.dp),
        contentAlignment = Alignment.Center
    ) {
        // Star shape drawing
        Canvas(modifier = Modifier.size(60.dp)) {
            val path = Path()
            val cx = size.width / 2
            val cy = size.height / 2
            val outerRadius = size.width / 2
            val innerRadius = size.width / 4
            val numPoints = 5

            for (i in 0 until numPoints * 2) {
                val radius = if (i % 2 == 0) outerRadius else innerRadius
                val angle = Math.PI / numPoints * i - Math.PI / 2
                val x = cx + (cos(angle) * radius).toFloat()
                val y = cy + (sin(angle) * radius).toFloat()
                if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
            }
            path.close()

            drawPath(path, color = NeonGreen, style = Stroke(width = 2.dp.toPx()))
            drawPath(path, color = NeonGreen.copy(alpha = 0.2f))
        }

        Text(text = text, color = NeonGreen)
    }
}

@Composable
fun SerpentineProgressBar(
    progress: Float,
    modifier: Modifier = Modifier
) {
    // Gradient simulating a flowing dragon/serpent
    val brush = Brush.horizontalGradient(
        colors = listOf(NeonGreen, SerpentineGreen, CyanBlue, ElectricPurple)
    )

    Column(modifier = modifier) {
        LinearProgressIndicator(
            progress = progress,
            modifier = Modifier
                .fillMaxWidth()
                .height(8.dp)
                .clip(CutCornerShape(4.dp)),
            color = NeonGreen, // Fallback
            trackColor = NeuralBlack
        )
        // Custom draw logic could be added here for more "serpentine" wave effects
    }
}

@Composable
fun HudHeader(title: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(modifier = Modifier.size(10.dp).background(NeonGreen))
        Spacer(modifier = Modifier.width(8.dp))
        Text(text = title.uppercase(), color = CyanBlue)
        Spacer(modifier = Modifier.weight(1f))
        Text(text = "NPU: ONLINE", color = NeonGreen)
    }
}
