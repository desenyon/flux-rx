# Flux-RX Themes Module: Visual styling configuration
from __future__ import annotations
from typing import Any

from flux_rx.exceptions import FluxThemeError

# Professional "Obsidian" theme (High-contrast dark, Bloomberg inspired)
OBSIDIAN_THEME: dict[str, Any] = {
    "name": "Obsidian",
    "colors": {
        "background": "#000000",
        "paper": "#0a0a0a",
        "surface": "#121212",
        "primary": "#38bdf8",  # Cyber Blue
        "secondary": "#34d399",  # Emerald
        "accent": "#cbd5e1",  # Slate light
        "warning": "#fbbf24",  # Amber
        "text": "#f1f5f9",
        "text_muted": "#94a3b8",
        "grid": "#1e293b",
        "border": "#273243",
        "positive": "#10b981",  # Green
        "negative": "#ef4444",  # Red
    },
    "palette": [
        "#38bdf8",
        "#34d399",
        "#cbd5e1",
        "#fbbf24",
        "#e2e8f0",
        "#94a3b8",
        "#10b981",
        "#0ea5e9",
    ],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#f1f5f9"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#ffffff"},
}

TERMINAL_THEME: dict[str, Any] = {
    "name": "Terminal",
    "colors": {
        "background": "#000000",
        "paper": "#050505",
        "surface": "#0a0a0a",
        "primary": "#00ff00",
        "secondary": "#00cc00",
        "accent": "#cccccc",
        "warning": "#ffaa00",
        "text": "#00ff00",
        "text_muted": "#008800",
        "grid": "#002200",
        "border": "#004400",
        "positive": "#00ff00",
        "negative": "#ff0000",
    },
    "palette": [
        "#00ff00",
        "#00cc00",
        "#ffffff",
        "#cccccc",
        "#008800",
        "#55ff55",
        "#004400",
        "#aaaaaa",
    ],
    "font": {"family": "JetBrains Mono, monospace", "size": 12, "color": "#00ff00"},
    "title_font": {"family": "JetBrains Mono, monospace", "size": 18, "color": "#00ff00"},
}

MONOCHROME_THEME: dict[str, Any] = {
    "name": "Monochrome",
    "colors": {
        "background": "#ffffff",
        "paper": "#f5f5f5",
        "surface": "#ebebeb",
        "primary": "#000000",
        "secondary": "#333333",
        "accent": "#666666",
        "warning": "#999999",
        "text": "#111111",
        "text_muted": "#777777",
        "grid": "#cccccc",
        "border": "#bbbbbb",
        "positive": "#111111",  # Differentiate by marker not color
        "negative": "#999999",
    },
    "palette": [
        "#000000",
        "#333333",
        "#666666",
        "#999999",
        "#222222",
        "#444444",
        "#888888",
        "#aaaaaa",
    ],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#111111"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#000000"},
}

LIGHT_PRO_THEME: dict[str, Any] = {
    "name": "Light Pro",
    "colors": {
        "background": "#ffffff",
        "paper": "#f8fafc",
        "surface": "#f1f5f9",
        "primary": "#0284c7",  # Sky darker
        "secondary": "#0f766e",  # Teal
        "accent": "#475569",  # Slate
        "warning": "#ca8a04",
        "text": "#0f172a",
        "text_muted": "#64748b",
        "grid": "#e2e8f0",
        "border": "#cbd5e1",
        "positive": "#15803d",
        "negative": "#b91c1c",
    },
    "palette": [
        "#0284c7",
        "#0f766e",
        "#475569",
        "#ca8a04",
        "#0369a1",
        "#0d9488",
        "#b91c1c",
        "#15803d",
    ],
    "font": {"family": "Inter, sans-serif", "size": 12, "color": "#0f172a"},
    "title_font": {"family": "Inter, sans-serif", "size": 18, "color": "#020617"},
}

_THEMES = {
    "obsidian": OBSIDIAN_THEME,
    "flux": OBSIDIAN_THEME,  # Fallback maps to Obsidian
    "terminal": TERMINAL_THEME,
    "monochrome": MONOCHROME_THEME,
    "light_pro": LIGHT_PRO_THEME,
    "light": LIGHT_PRO_THEME,  # Fallback maps to Light Pro
}

DEFAULT_THEME = "obsidian"


def get_theme(name: str = DEFAULT_THEME) -> dict[str, Any]:
    """Get the theme configuration by name."""
    theme = _THEMES.get(name.lower())
    if theme is None:
        raise FluxThemeError(f"Unknown theme: '{name}'. Available: {list_themes()}")
    return theme


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

    is_dark = theme in [OBSIDIAN_THEME, TERMINAL_THEME]

    return {
        "template": "plotly_dark" if is_dark else "plotly_white",
        "paper_bgcolor": colors["paper"],
        "plot_bgcolor": colors["background"],
        "height": height,
        "margin": {"l": 60, "r": 30, "t": 60 if title else 30, "b": 50},
        "title": (
            {
                "text": title,
                "font": title_font,
                "x": 0.02,
                "xanchor": "left",
            }
            if title
            else None
        ),
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

    if theme in [LIGHT_PRO_THEME, MONOCHROME_THEME]:
        return [
            [0.0, colors["negative"]],
            [0.35, "#f1f5f9"],
            [0.5, "#ffffff"],
            [0.65, "#dcfce7"],
            [1.0, colors["positive"]],
        ]

    return [
        [0.0, colors["negative"]],
        [0.35, "#1f2937"],
        [0.5, colors["surface"]],
        [0.65, "#064e3b"],
        [1.0, colors["positive"]],
    ]
