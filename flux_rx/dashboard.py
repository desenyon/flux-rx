# Flux-RX Dashboard Module: Interactive Dash application
from __future__ import annotations

from typing import Optional

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc

from flux_rx.data import fetch, get_info, fetch_multiple, align_dataframes
from flux_rx.analytics import compute_metrics, format_metrics
from flux_rx.charts import (
    price_chart,
    drawdown_chart,
    monthly_heatmap,
    performance_chart,
    correlation_matrix,
    cumulative_returns_chart,
)
from flux_rx.themes import get_theme, list_themes, DEFAULT_THEME

# --- SIDEBAR STYLE ---
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#0f172a",  # Dark Slate
    "color": "#f8fafc",
    "borderRight": "1px solid #1e293b",
    "zIndex": 1000,
}

# --- CONTENT STYLE ---
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "padding": "2rem 3rem",
    "minHeight": "100vh",
    "backgroundColor": "#020617",  # Deeper Slate for main BG
    "color": "#f1f5f9",
}


def create_app(
    default_tickers: Optional[list[str]] = None,
    default_theme: str = DEFAULT_THEME,
) -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        title="Flux-RX Terminal Dashboard",
    )

    if default_tickers is None:
        default_tickers = ["SPY"]

    sidebar = html.Div(
        [
            html.H2(
                "FLUX-RX",
                className="display-6",
                style={"fontWeight": "800", "letterSpacing": "1px"},
            ),
            html.P(
                "v2.0.0 Terminal Engine", className="lead text-muted", style={"fontSize": "0.85rem"}
            ),
            html.Hr(style={"borderColor": "#334155"}),
            dbc.Nav(
                [
                    dbc.NavLink(
                        "Single Ticker Analysis",
                        href="/",
                        active="exact",
                        id="nav-single",
                        style={"color": "#94a3b8"},
                    ),
                    dbc.NavLink(
                        "Multi-Ticker Comparison",
                        href="/compare",
                        active="exact",
                        id="nav-compare",
                        style={"color": "#94a3b8"},
                    ),
                ],
                vertical=True,
                pills=True,
                className="mb-4",
            ),
            html.Hr(style={"borderColor": "#334155"}),
            html.P(
                "Theme Settings",
                className="text-muted",
                style={"fontSize": "0.75rem", "textTransform": "uppercase", "letterSpacing": "1px"},
            ),
            dcc.Dropdown(
                id="global-theme-selector",
                options=[{"label": t.title().replace("_", " "), "value": t} for t in list_themes()],
                value=default_theme,
                clearable=False,
                style={"color": "#000000"},  # Ensure dropdown text is visible
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

    @app.callback(
        Output("nav-single", "active"), Output("nav-compare", "active"), Input("url", "pathname")
    )
    def update_sidebar_active(pathname):
        if pathname == "/compare":
            return False, True
        return True, False

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/compare":
            return render_compare_view()
        # Default to single view
        return render_single_view()

    @app.callback(
        [
            Output("single-metrics-summary", "children"),
            Output("single-charts-container", "children"),
        ],
        [Input("analyze-btn", "n_clicks")],
        [
            State("ticker-input", "value"),
            State("period-selector", "value"),
            State("global-theme-selector", "value"),
        ],
    )
    def update_single(n_clicks, ticker, period, theme):
        if not ticker:
            return no_update, no_update
        ticker = ticker.upper().strip()
        try:
            df = fetch(ticker, period=period)
            metrics = compute_metrics(df["Close"])
            formatted = format_metrics(metrics)

            # Use theme from the file to match colors
            theme_config = get_theme(theme)
            bg_color = theme_config["colors"]["surface"]
            border_color = theme_config["colors"]["border"]

            card_style = {
                "backgroundColor": bg_color,
                "border": f"1px solid {border_color}",
                "borderRadius": "4px",
                "marginBottom": "1rem",
            }

            summary = dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "CAGR",
                                        className="text-muted text-uppercase",
                                        style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                                    ),
                                    html.H3(
                                        formatted["cagr"],
                                        style={
                                            "color": (
                                                theme_config["colors"]["positive"]
                                                if metrics["cagr"] >= 0
                                                else theme_config["colors"]["negative"]
                                            ),
                                            "fontFamily": "monospace",
                                        },
                                    ),
                                ]
                            ),
                            style=card_style,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Volatility",
                                        className="text-muted text-uppercase",
                                        style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                                    ),
                                    html.H3(
                                        formatted["volatility"],
                                        style={
                                            "fontFamily": "monospace",
                                            "color": theme_config["colors"]["text"],
                                        },
                                    ),
                                ]
                            ),
                            style=card_style,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Sharpe Ratio",
                                        className="text-muted text-uppercase",
                                        style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                                    ),
                                    html.H3(
                                        formatted["sharpe_ratio"],
                                        style={
                                            "fontFamily": "monospace",
                                            "color": theme_config["colors"]["text"],
                                        },
                                    ),
                                ]
                            ),
                            style=card_style,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Max Drawdown",
                                        className="text-muted text-uppercase",
                                        style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                                    ),
                                    html.H3(
                                        formatted["max_drawdown"],
                                        style={
                                            "color": theme_config["colors"]["negative"],
                                            "fontFamily": "monospace",
                                        },
                                    ),
                                ]
                            ),
                            style=card_style,
                        ),
                        width=3,
                    ),
                ]
            )

            charts = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=price_chart(
                                        df, ticker=ticker, theme=theme, height=450, show_volume=True
                                    )
                                ),
                                width=12,
                            ),
                        ],
                        className="mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=cumulative_returns_chart(
                                        df["Close"], ticker=ticker, theme=theme, height=400
                                    )
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    figure=drawdown_chart(
                                        df["Close"], ticker=ticker, theme=theme, height=400
                                    )
                                ),
                                width=6,
                            ),
                        ],
                        className="mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=monthly_heatmap(
                                        df["Close"], ticker=ticker, theme=theme, height=400
                                    )
                                ),
                                width=12,
                            ),
                        ]
                    ),
                ]
            )

            return summary, charts
        except Exception as e:
            return dbc.Alert(f"System Error: {str(e)}", color="danger"), []

    @app.callback(
        Output("compare-results", "children"),
        [Input("compare-btn", "n_clicks")],
        [
            State("tickers-input", "value"),
            State("compare-period-selector", "value"),
            State("global-theme-selector", "value"),
        ],
    )
    def update_compare(n_clicks, tickers_str, period, theme):
        if not tickers_str:
            return no_update
        tickers = [t.strip().upper() for t in tickers_str.split(",") if t.strip()]
        if len(tickers) < 2:
            return dbc.Alert("Please enter at least two tickers.", color="warning")

        try:
            data = fetch_multiple(tickers, period=period)
            prices_df = align_dataframes(data)

            perf_fig = performance_chart(
                {t: prices_df[t] for t in tickers}, theme=theme, height=500
            )
            corr_fig = correlation_matrix(prices_df, theme=theme, height=500)

            return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(figure=perf_fig), width=12),
                        ],
                        className="mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(figure=corr_fig), width=12),
                        ]
                    ),
                ]
            )
        except Exception as e:
            return dbc.Alert(f"System Error: {str(e)}", color="danger")

    return app


def render_single_view():
    return html.Div(
        [
            html.H3("Ticker Analysis", style={"marginBottom": "2rem", "fontWeight": "600"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(
                                "Ticker Symbol",
                                className="text-muted text-uppercase",
                                style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                            ),
                            dbc.Input(
                                id="ticker-input",
                                value="AAPL",
                                placeholder="e.g. MSFT",
                                style={
                                    "backgroundColor": "transparent",
                                    "color": "inherit",
                                    "borderRadius": "0",
                                },
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Label(
                                "Time Period",
                                className="text-muted text-uppercase",
                                style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                            ),
                            dbc.Select(
                                id="period-selector",
                                options=[
                                    {"label": "1 Year", "value": "1y"},
                                    {"label": "2 Years", "value": "2y"},
                                    {"label": "5 Years", "value": "5y"},
                                    {"label": "10 Years", "value": "10y"},
                                    {"label": "Maximum", "value": "max"},
                                ],
                                value="5y",
                                style={"backgroundColor": "transparent", "color": "inherit"},
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Div(style={"height": "1.5rem"}),  # Spacer
                            dbc.Button(
                                "Execute",
                                id="analyze-btn",
                                color="primary",
                                style={
                                    "width": "100%",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "1px",
                                    "borderRadius": "2px",
                                },
                            ),
                        ],
                        width=2,
                    ),
                ],
                className="mb-5",
            ),
            html.Div(id="single-metrics-summary"),
            html.Div(id="single-charts-container"),
        ]
    )


def render_compare_view():
    return html.Div(
        [
            html.H3(
                "Correlation & Performance Comparison",
                style={"marginBottom": "2rem", "fontWeight": "600"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(
                                "Tickers (comma separated)",
                                className="text-muted text-uppercase",
                                style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                            ),
                            dbc.Input(
                                id="tickers-input",
                                value="AAPL, MSFT, GOOGL",
                                placeholder="AAPL, TSLA",
                                style={
                                    "backgroundColor": "transparent",
                                    "color": "inherit",
                                    "borderRadius": "0",
                                },
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Label(
                                "Time Period",
                                className="text-muted text-uppercase",
                                style={"fontSize": "0.75rem", "letterSpacing": "1px"},
                            ),
                            dbc.Select(
                                id="compare-period-selector",
                                options=[
                                    {"label": "1 Year", "value": "1y"},
                                    {"label": "5 Years", "value": "5y"},
                                    {"label": "10 Years", "value": "10y"},
                                ],
                                value="5y",
                                style={"backgroundColor": "transparent", "color": "inherit"},
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Div(style={"height": "1.5rem"}),  # Spacer
                            dbc.Button(
                                "Compare",
                                id="compare-btn",
                                color="success",
                                style={
                                    "width": "100%",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "1px",
                                    "borderRadius": "2px",
                                },
                            ),
                        ],
                        width=3,
                    ),
                ],
                className="mb-5",
            ),
            html.Div(id="compare-results"),
        ]
    )
