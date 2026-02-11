# Flux-RX Themes Module: Visual styling configuration
from __future__ import annotations
from typing import Any

# Default "flux" theme (previously THEME)
FLUX_THEME: dict[str, Any] = {
    "name": "Flux",
    "colors": {
        "background": "#0d1117",
        "paper": "#161b22",
        "surface": "#21262d",
        "primary": "#58a6ff",
        "secondary": "#7ee787",
        "accent": "#ff7b72",
        "warning": "#d29922",
        "text": "#c9d1d9",
        "text_muted": "#8b949e",
        "grid": "#30363d",
        "border": "#30363d",
        "positive": "#3fb950",
        "negative": "#f85149",
    },
    "palette": ["#58a6ff", "#7ee787", "#ff7b72", "#d2a8ff", "#79c0ff", "#ffa657", "#a5d6ff", "#f778ba"],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#c9d1d9"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#ffffff"},
}

MIDNIGHT_THEME: dict[str, Any] = {
    "name": "Midnight",
    "colors": {
        "background": "#05070a",
        "paper": "#0a0c10",
        "surface": "#12151c",
        "primary": "#38bdf8",
        "secondary": "#34d399",
        "accent": "#f472b6",
        "warning": "#fbbf24",
        "text": "#e2e8f0",
        "text_muted": "#94a3b8",
        "grid": "#1e293b",
        "border": "#1e293b",
        "positive": "#10b981",
        "negative": "#ef4444",
    },
    "palette": ["#38bdf8", "#34d399", "#f472b6", "#fbbf24", "#818cf8", "#c084fc", "#fb7185", "#2dd4bf"],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#e2e8f0"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#ffffff"},
}

LIGHT_THEME: dict[str, Any] = {
    "name": "Light",
    "colors": {
        "background": "#ffffff",
        "paper": "#f8fafc",
        "surface": "#f1f5f9",
        "primary": "#2563eb",
        "secondary": "#10b981",
        "accent": "#f43f5e",
        "warning": "#d97706",
        "text": "#1e293b",
        "text_muted": "#64748b",
        "grid": "#e2e8f0",
        "border": "#e2e8f0",
        "positive": "#16a34a",
        "negative": "#dc2626",
    },
    "palette": ["#2563eb", "#10b981", "#f43f5e", "#d97706", "#7c3aed", "#0891b2", "#db2777", "#4f46e5"],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#1e293b"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#0f172a"},
}

TERMINAL_THEME: dict[str, Any] = {
    "name": "Terminal",
    "colors": {
        "background": "#000000",
        "paper": "#0a0a0a",
        "surface": "#1a1a1a",
        "primary": "#00ff00",
        "secondary": "#00cc00",
        "accent": "#ffff00",
        "warning": "#ffaa00",
        "text": "#00ff00",
        "text_muted": "#00aa00",
        "grid": "#003300",
        "border": "#005500",
        "positive": "#00ff00",
        "negative": "#ff0000",
    },
    "palette": ["#00ff00", "#ffff00", "#00ffff", "#ff00ff", "#0088ff", "#ff8800", "#ffffff", "#888888"],
    "font": {"family": "JetBrains Mono, monospace", "size": 12, "color": "#00ff00"},
    "title_font": {"family": "JetBrains Mono, monospace", "size": 18, "color": "#00ff00"},
}

_THEMES = {
    "flux": FLUX_THEME,
    "glass": FLUX_THEME,  # Alias
    "midnight": MIDNIGHT_THEME,
    "light": LIGHT_THEME,
    "terminal": TERMINAL_THEME,
}

DEFAULT_THEME = "flux"


def get_theme(name: str = DEFAULT_THEME) -> dict[str, Any]:
    """Get the theme configuration by name."""
    return _THEMES.get(name.lower(), FLUX_THEME)


def list_themes() -> list[str]:
    """List available themes."""
    return list(_THEMES.keys())


def create_layout(
    theme: dict[str, Any],
    title: str = "",
    height: int = 500,
    show_legend: bool = True,
    x_title: str = "",
    y_title: str = "",
) -> dict[str, Any]:
    """Create a Plotly layout from theme configuration."""
    colors = theme["colors"]
    font = theme["font"]
    title_font = theme["title_font"]
    
    is_dark = theme != LIGHT_THEME
    
    return {
        "template": "plotly_dark" if is_dark else "plotly_white",
        "paper_bgcolor": colors["paper"],
        "plot_bgcolor": colors["background"],
        "height": height,
        "margin": {"l": 60, "r": 30, "t": 60 if title else 30, "b": 50},
        "title": {
            "text": title,
            "font": title_font,
            "x": 0.02,
            "xanchor": "left",
        } if title else None,
        "font": font,
        "showlegend": show_legend,
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "font": {"color": colors["text"], "size": 11},
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        "xaxis": {
            "title": {"text": x_title, "font": {"color": colors["text_muted"]}},
            "gridcolor": colors["grid"],
            "gridwidth": 1,
            "linecolor": colors["border"],
            "tickfont": {"color": colors["text_muted"], "size": 10},
            "zeroline": False,
            "showspikes": True,
            "spikecolor": colors["primary"],
            "spikethickness": 1,
            "spikedash": "dot",
            "spikemode": "across",
        },
        "yaxis": {
            "title": {"text": y_title, "font": {"color": colors["text_muted"]}},
            "gridcolor": colors["grid"],
            "gridwidth": 1,
            "linecolor": colors["border"],
            "tickfont": {"color": colors["text_muted"], "size": 10},
            "zeroline": False,
            "side": "right",
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": colors["surface"],
            "bordercolor": colors["border"],
            "font": {"color": colors["text"], "size": 12},
        },
    }


def apply_theme(fig: Any, name: str = DEFAULT_THEME) -> Any:
    """Apply a theme to a Plotly figure."""
    theme = get_theme(name)
    layout = create_layout(theme)
    fig.update_layout(**layout)
    return fig


def get_heatmap_colorscale(name: str = DEFAULT_THEME) -> list:
    """Get the colorscale for monthly returns heatmap."""
    theme = get_theme(name)
    colors = theme["colors"]
    
    if theme == LIGHT_THEME:
        return [
            [0.0, "#b91c1c"],
            [0.35, "#fee2e2"],
            [0.5, "#ffffff"],
            [0.65, "#dcfce7"],
            [1.0, "#15803d"],
        ]
    
    return [
        [0.0, colors["negative"]],
        [0.35, "#3d1f1f"],
        [0.5, colors["surface"]],
        [0.65, "#1f3d1f"],
        [1.0, colors["positive"]],
    ]
