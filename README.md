# Flux-RX

> High-Performance Financial Engineering & Analytics Framework

**Flux-RX** is an advanced, institutional-grade Python framework designed for rapid financial data analysis, portfolio optimization, and beautifully rendered interactive dashboards. Replacing disjointed scripts with a cohesive system, Flux-RX implements strict typing, rigorous error handling, and a sophisticated terminal UI.

---

## Capabilities

*   **Robust Data Ingestion**: High-speed, cached acquisition of market data and metadata via Yahoo Finance.
*   **Deep Analytics Engine**: Compute comprehensive metrics including CAGR, Volatility, Sharpe Ratio, Maximum Drawdown, Value at Risk (VaR), Conditional VaR, Information Ratio, Tracking Error, Hurst Exponent, and Z-Scores.
*   **Terminal Interface**: A best-in-class CLI built on `rich` that renders stunning, color-coded tables for metrics, screening, and optimization natively in the console.
*   **Dynamic Dashboard**: A fully responsive, sidebar-navigation local web application (`dash-bootstrap-components`) for profound visual analysis.
*   **Hyper-Professional Layouts**: Native support for "Obsidian", "Terminal", "Monochrome", and "Light Pro" themes. Strictly adhering to institutional aesthetics (no emojis, no purple elements).
*   **Portfolio Architecture**: Conduct Modern Portfolio Theory (MPT) optimization targeting Maximum Sharpe, Minimum Volatility, or Maximum Return.

## Installation

Ensure you have Python 3.10+ installed.

```bash
# Clone the repository
git clone https://github.com/your-org/flux-rx.git
cd flux-rx

# Install via setup.py (or pip)
pip install -e .
```

*Note: For development capabilities (like `mypy` and `pytest`), install with `pip install -e .[dev]`.*

## Command-Line Interface

The `flux-rx` command serves as your entry point to all operations.

### Quick Metrics
Extract fundamental metrics and calculate ratios instantly.
```bash
flux-rx metrics AAPL --period 5y
```

### Portfolio Screener
Compare, rank, and evaluate multiple assets simultaneously.
```bash
flux-rx screen AAPL MSFT GOOGL NVDA TSLA --sort sharpe_ratio
```

### Modern Portfolio Optimization
Calculate the optimal weightings for a basket of assets.
```bash
flux-rx optimize AAPL MSFT GOOGL --objective sharpe
```

### Static Reporting & Export
Generate a sleek static HTML report or export raw data to your preferred format.
```bash
# Generate interactive HTML report
flux-rx report AAPL --period max --theme obsidian

# Export to CSV/JSON/Excel
flux-rx export AAPL --format csv --path my_data.csv
```

### Interactive Dashboard
Launch the heavy-duty analytical terminal in your browser.
```bash
flux-rx dashboard --port 8050
```

## System Architecture

Flux-RX v2.0 introduces several architectural upgrades:
*   **`flux_rx.exceptions`**: A custom exception hierarchy (`FluxDataError`, `FluxComputeError`, etc.) ensuring graceful failure states without arbitrary Python stack traces.
*   **`flux_rx.logger`**: Structured, console-agnostic logging powered by `rich`, replacing arbitrary `print` statements.
*   **`flux_rx.analytics`**: Hardened numerical methods with explicit input validation on raw price vectors.

## License

MIT License. See `LICENSE` for details.
