# Flux-RX Report Module: Publication-quality interactive HTML report generation
from __future__ import annotations

from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from flux_rx.analytics import (
    compute_metrics,
    format_metrics,
    monthly_returns,
    drawdown_series,
    rolling_volatility,
    rolling_sharpe,
    daily_returns,
    cumulative_returns,
)
from flux_rx.data import get_info, fetch
from flux_rx.themes import get_theme, DEFAULT_THEME, get_heatmap_colorscale


def _create_main_chart(df: pd.DataFrame, ticker: str, theme_config: dict) -> go.Figure:
    colors = theme_config["colors"]
    palette = theme_config["palette"]

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.6, 0.2, 0.2],
        specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC",
            increasing={
                "line": {"color": colors["positive"], "width": 1},
                "fillcolor": colors["positive"],
            },
            decreasing={
                "line": {"color": colors["negative"], "width": 1},
                "fillcolor": colors["negative"],
            },
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    for i, window in enumerate([20, 50, 200]):
        if len(df) >= window:
            ma = df["Close"].rolling(window=window).mean()
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=ma,
                    mode="lines",
                    name=f"MA{window}",
                    line={"color": palette[i % len(palette)], "width": 1.5},
                    hovertemplate=f"MA{window}: $%{{y:.2f}}<extra></extra>",
                ),
                row=1,
                col=1,
            )

    volume_colors = [
        colors["positive"] if df["Close"].iloc[i] >= df["Open"].iloc[i] else colors["negative"]
        for i in range(len(df))
    ]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
            marker_color=volume_colors,
            opacity=0.7,
            showlegend=False,
            hovertemplate="Vol: %{y:,.0f}<extra></extra>",
        ),
        row=2,
        col=1,
    )

    dd = drawdown_series(df["Close"])
    fig.add_trace(
        go.Scatter(
            x=dd.index,
            y=dd * 100,
            mode="lines",
            name="Drawdown",
            fill="tozeroy",
            line={"color": colors["negative"], "width": 1},
            fillcolor=f"rgba({int(colors['negative'][1:3], 16)}, {int(colors['negative'][3:5], 16)}, {int(colors['negative'][5:7], 16)}, 0.4)",
            showlegend=False,
            hovertemplate="DD: %{y:.2f}%<extra></extra>",
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=650,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        font={"family": "Inter, sans-serif", "color": colors["text"]},
        showlegend=True,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 11},
        },
        hovermode="x unified",
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        xaxis2={"showgrid": False, "zeroline": False, "showticklabels": False},
        xaxis3={"showgrid": True, "gridcolor": colors["grid"], "zeroline": False},
        yaxis={
            "showgrid": True,
            "gridcolor": colors["grid"],
            "zeroline": False,
            "side": "right",
            "tickformat": "$,.0f",
        },
        yaxis2={"showgrid": False, "zeroline": False, "side": "right", "tickformat": ".2s"},
        yaxis3={
            "showgrid": True,
            "gridcolor": colors["grid"],
            "zeroline": True,
            "zerolinecolor": colors["grid"],
            "side": "right",
            "ticksuffix": "%",
        },
    )

    return fig


def _create_analytics_charts(
    prices: pd.Series, benchmark_prices: Optional[pd.Series], theme_config: dict
) -> go.Figure:
    colors = theme_config["colors"]

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Cumulative Returns",
            "Rolling Volatility (21D)",
            "Rolling Sharpe (63D)",
            "Returns Distribution",
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )

    cum_ret = cumulative_returns(prices) * 100
    fig.add_trace(
        go.Scatter(
            x=cum_ret.index, y=cum_ret, name="Asset", line_color=colors["accent"], fill="tozeroy"
        ),
        row=1,
        col=1,
    )

    vol = rolling_volatility(prices) * 100
    fig.add_trace(
        go.Scatter(x=vol.index, y=vol, name="Volatility", line_color=colors["secondary"]),
        row=1,
        col=2,
    )

    sharpe = rolling_sharpe(prices)
    fig.add_trace(
        go.Scatter(x=sharpe.index, y=sharpe, name="Sharpe", line_color=colors["positive"]),
        row=2,
        col=1,
    )

    rets = daily_returns(prices) * 100
    fig.add_trace(
        go.Histogram(x=rets, name="Distribution", marker_color=colors["accent"]), row=2, col=2
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=500,
        showlegend=False,
    )
    return fig


def _create_heatmap(
    prices: pd.Series, theme_config: dict, theme_name: str = DEFAULT_THEME
) -> go.Figure:
    colors = theme_config["colors"]
    monthly_df = monthly_returns(prices)
    z_values = monthly_df.values * 100

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=monthly_df.columns,
            y=[str(y) for y in monthly_df.index],
            colorscale=get_heatmap_colorscale(theme_name),
            text=[[f"{v:.1f}%" if not np.isnan(v) else "" for v in row] for row in z_values],
            texttemplate="%{text}",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
    )
    return fig


from flux_rx.report_styles import BASE_CSS, COMPARISON_CSS
from flux_rx.report_templates import SINGLE_REPORT_TEMPLATE, COMPARISON_REPORT_TEMPLATE


def generate_report(
    ticker: str,
    period: str = "5y",
    benchmark: Optional[str] = None,
    theme: str = DEFAULT_THEME,
    save: Optional[str] = None,
) -> str:
    """Generate a high-quality interactive HTML report for a ticker."""
    try:
        theme_config = get_theme(theme)
        df = fetch(ticker, period=period)
        if df.empty:
            raise ValueError(f"No data for {ticker}")
        prices = df["Close"]
        info = get_info(ticker)

        benchmark_prices = None
        if benchmark:
            try:
                benchmark_df = fetch(benchmark, period=period)
                aligned_idx = prices.index.intersection(benchmark_df.index)
                prices = prices.loc[aligned_idx]
                benchmark_prices = benchmark_df["Close"].loc[aligned_idx]
                df = df.loc[aligned_idx]
            except:
                benchmark = None

        metrics = compute_metrics(prices, benchmark_prices)
        formatted = format_metrics(metrics)

        main_chart = _create_main_chart(df, ticker, theme_config)
        analytics_chart = _create_analytics_charts(prices, benchmark_prices, theme_config)
        heatmap_chart = _create_heatmap(prices, theme_config, theme)

        cards = "".join(
            [
                f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{formatted.get(k, "N/A")}</div></div>'
                for l, k in [
                    ("CAGR", "cagr"),
                    ("Vol", "volatility"),
                    ("Sharpe", "sharpe_ratio"),
                    ("Max DD", "max_drawdown"),
                ]
            ]
        )

        rows = "".join(
            [
                f'<div class="info-row"><span class="info-label">{l}</span><span class="info-value">{info.get(k, "N/A")}</span></div>'
                for l, k in [
                    ("Industry", "industry"),
                    ("Sector", "sector"),
                    ("Cap", "market_cap_fmt"),
                    ("Market", "exchange"),
                ]
            ]
        )

        current_price = float(prices.iloc[-1])
        prev_price = float(prices.iloc[-2]) if len(prices) > 1 else current_price
        day_change = (current_price - prev_price) / prev_price * 100

        html = SINGLE_REPORT_TEMPLATE.format(
            ticker=ticker,
            ticker_name=info.get("name", ticker),
            ticker_sector=info.get("sector", "Equity"),
            ticker_description=info.get("description", "Analysis by Flux-RX."),
            css=BASE_CSS,
            metric_cards=cards,
            main_chart_html=main_chart.to_html(full_html=False, include_plotlyjs=False),
            analytics_chart_html=analytics_chart.to_html(full_html=False, include_plotlyjs=False),
            heatmap_chart_html=heatmap_chart.to_html(full_html=False, include_plotlyjs=False),
            security_info_rows=rows,
            current_price=current_price,
            change_class="positive" if day_change >= 0 else "negative",
            change_bg_class="positive-bg" if day_change >= 0 else "negative-bg",
            change_abs=abs(current_price - prev_price),
            change_pct=day_change,
            change_sign="+" if day_change >= 0 else "",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        if save:
            with open(save, "w", encoding="utf-8") as f:
                f.write(html)
        return html
    except Exception as e:
        return f"<html><body style='background:#09090b;color:#fafafa;padding:40px;font-family:sans-serif'><h1>Report Error</h1><p>{str(e)}</p></body></html>"


def generate_comparison_report(
    tickers: list[str],
    period: str = "5y",
    theme: str = DEFAULT_THEME,
    save: Optional[str] = None,
) -> str:
    """Generate a multi-ticker comparison report."""
    try:
        from flux_rx.data import fetch_multiple, align_dataframes

        theme_config = get_theme(theme)
        palette = theme_config["palette"]

        data = fetch_multiple(tickers, period=period)
        prices_df = align_dataframes(data)
        if prices_df.empty:
            raise ValueError("No overlapping data.")

        all_metrics = {t: compute_metrics(prices_df[t]) for t in tickers}

        perf_fig = go.Figure()
        for i, t in enumerate(tickers):
            norm = (prices_df[t] / prices_df[t].iloc[0] - 1) * 100
            perf_fig.add_trace(
                go.Scatter(x=norm.index, y=norm, name=t, line_color=palette[i % len(palette)])
            )
        perf_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
        )

        from flux_rx.charts import risk_return_scatter, correlation_matrix

        risk_fig = risk_return_scatter(all_metrics, theme=theme, height=400)
        corr_fig = correlation_matrix(prices_df, theme=theme, height=400)

        m_rows = "".join(
            [
                f"<tr><td>{t}</td><td>{format_metrics(all_metrics[t])['cagr']}</td><td>{format_metrics(all_metrics[t])['volatility']}</td><td>{format_metrics(all_metrics[t])['max_drawdown']}</td><td>{format_metrics(all_metrics[t])['sharpe_ratio']}</td><td>{format_metrics(all_metrics[t])['sortino_ratio']}</td><td>{format_metrics(all_metrics[t])['calmar_ratio']}</td></tr>"
                for t in tickers
            ]
        )
        badges = "".join(
            [
                f'<span class="ticker-badge" style="border-left: 3px solid {palette[i % len(palette)]}">{t}</span>'
                for i, t in enumerate(tickers)
            ]
        )

        html = COMPARISON_REPORT_TEMPLATE.format(
            css=COMPARISON_CSS,
            start_date=prices_df.index[0].strftime("%b %d, %Y"),
            end_date=prices_df.index[-1].strftime("%b %d, %Y"),
            ticker_badges=badges,
            metrics_rows=m_rows,
            perf_html=perf_fig.to_html(full_html=False, include_plotlyjs=False),
            risk_html=risk_fig.to_html(full_html=False, include_plotlyjs=False),
            corr_html=corr_fig.to_html(full_html=False, include_plotlyjs=False),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        if save:
            with open(save, "w", encoding="utf-8") as f:
                f.write(html)
        return html
    except Exception as e:
        return f"<html><body style='background:#09090b;color:#fafafa;padding:40px;font-family:sans-serif'><h1>Comparison Error</h1><p>{str(e)}</p></body></html>"
