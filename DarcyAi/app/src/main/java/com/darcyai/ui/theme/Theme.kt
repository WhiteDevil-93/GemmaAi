package com.darcyai.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

// Force Dark Theme for Cyberpunk aesthetic
private val DarkColorScheme = darkColorScheme(
    primary = NeonGreen,
    secondary = ElectricPurple,
    tertiary = CyanBlue,
    background = NeuralBlack,
    surface = NeuralBlack,
    onPrimary = NeuralBlack,
    onSecondary = TextWhite,
    onTertiary = NeuralBlack,
    onBackground = TextWhite,
    onSurface = TextWhite,
)

@Composable
fun DarcyAiTheme(
    darkTheme: Boolean = isSystemInDarkTheme(), // Always tends to dark in this app
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = false, // Disable dynamic color to enforce branding
    content: @Composable () -> Unit
) {
    val colorScheme = DarkColorScheme

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
