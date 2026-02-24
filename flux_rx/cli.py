# Flux-RX CLI Module: Command-line interface
from __future__ import annotations

import argparse
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from flux_rx import __version__, quick, metrics, info, chart, app, screen, optimize, export

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description=f"Flux-RX Finance CLI v{__version__}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"flux-rx {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate analysis report")
    report_parser.add_argument("ticker", help="Stock symbol (e.g., AAPL)")
    report_parser.add_argument("--period", default="5y", help="Time period")
    report_parser.add_argument("--benchmark", help="Benchmark symbol")
    report_parser.add_argument("--theme", default="flux", help="Visual theme")
    report_parser.add_argument("--save", help="Save report to file")
    report_parser.add_argument("--no-show", action="store_true", help="Don't open in browser")

    # Metrics command
    metrics_parser = subparsers.add_parser("metrics", help="Show financial metrics")
    metrics_parser.add_argument("ticker", help="Stock symbol")
    metrics_parser.add_argument("--period", default="5y", help="Time period")
    metrics_parser.add_argument("--benchmark", help="Benchmark symbol")
    metrics_parser.add_argument("--raw", action="store_true", help="Show raw values")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show company information")
    info_parser.add_argument("ticker", help="Stock symbol")

    # Dashboard command
    dash_parser = subparsers.add_parser("dashboard", help="Launch interactive dashboard")
    dash_parser.add_argument("--port", type=int, default=8050, help="Port number")
    dash_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Screen command
    screen_parser = subparsers.add_parser("screen", help="Screen and rank stocks")
    screen_parser.add_argument("tickers", nargs="+", help="List of tickers")
    screen_parser.add_argument("--period", default="1y", help="Time period")
    screen_parser.add_argument("--sort", default="sharpe_ratio", help="Metric to sort by")

    # Optimize command
    optimize_parser = subparsers.add_parser("optimize", help="Optimize a portfolio")
    optimize_parser.add_argument("tickers", nargs="+", help="List of tickers")
    optimize_parser.add_argument("--period", default="5y", help="Lookback period")
    optimize_parser.add_argument(
        "--objective", default="sharpe", help="sharpe, min_vol, or max_return"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export ticker data to file")
    export_parser.add_argument("ticker", help="Stock symbol")
    export_parser.add_argument("--format", default="csv", help="csv, json, or excel")
    export_parser.add_argument("--path", help="Output file path")
    export_parser.add_argument("--period", default="5y", help="Time period")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "report":
            console.print(f"[bold cyan]Generating report for {args.ticker.upper()}...[/bold cyan]")
            save_path = args.save or f"{args.ticker}_report.html"
            quick(
                args.ticker,
                period=args.period,
                benchmark=args.benchmark,
                theme=args.theme,
                save=save_path,
                show=not args.no_show,
            )
            console.print(
                f"[bold green]SUCCESS:[/bold green] Report saved to [underline]{os.path.abspath(save_path)}[/underline]"
            )

        elif args.command == "metrics":
            data = metrics(
                args.ticker, period=args.period, benchmark=args.benchmark, formatted=not args.raw
            )
            table = Table(
                title=f"Metrics for {args.ticker.upper()} ({args.period})",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")

            for k, v in data.items():
                table.add_row(k.replace("_", " ").title(), str(v))

            console.print(table)

        elif args.command == "info":
            data = info(args.ticker)
            table = Table(
                title=f"Company Info: {args.ticker.upper()}",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Attribute", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")

            for k, v in data.items():
                if k != "description":
                    table.add_row(k.replace("_", " ").title(), str(v))

            console.print(table)

            if data.get("description"):
                desc = data["description"]
                short_desc = desc[:500] + ("..." if len(desc) > 500 else "")
                panel = Panel(short_desc, title="Description", border_style="cyan")
                console.print(panel)

        elif args.command == "dashboard":
            console.print(
                f"[bold cyan]Launching Flux-RX Terminal on port {args.port}...[/bold cyan]"
            )
            app(port=args.port, debug=args.debug)

        elif args.command == "screen":
            console.print(
                f"[bold cyan]Screening {len(args.tickers)} tickers over {args.period}...[/bold cyan]"
            )
            df = screen(args.tickers, period=args.period, sort_by=args.sort)
            table = Table(
                title=f"Screener Results (Ranked by {args.sort})",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Rank", justify="right", style="cyan")
            table.add_column("Ticker", style="bold white")
            table.add_column("CAGR", justify="right", style="green")
            table.add_column("Sharpe", justify="right")
            table.add_column("Max DD", justify="right", style="red")

            for i, (ticker, row) in enumerate(df.head(10).iterrows(), 1):
                table.add_row(
                    str(i),
                    str(ticker),
                    f"{row['cagr']*100:.2f}%",
                    f"{row['sharpe_ratio']:.2f}",
                    f"{row['max_drawdown']*100:.2f}%",
                )
            console.print(table)

        elif args.command == "optimize":
            console.print(
                f"[bold cyan]Optimizing portfolio for {len(args.tickers)} tickers...[/bold cyan]"
            )
            results = optimize(args.tickers, period=args.period, objective=args.objective)
            table = Table(
                title=f"Optimal Weights ({args.objective.upper()})",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("Ticker", style="cyan")
            table.add_column("Weight", justify="right", style="green")

            for ticker, weight in results["weights"].items():
                if weight > 0.001:  # Only show meaningful weights
                    table.add_row(ticker, f"{weight*100:.2f}%")

            console.print(table)
            console.print(
                f"[bold white]Expected Return:[/bold white] [green]{results['return']*100:.2f}%[/green]"
            )
            console.print(
                f"[bold white]Expected Volatility:[/bold white] {results['volatility']*100:.2f}%"
            )
            console.print(f"[bold white]Sharpe Ratio:[/bold white] {results['sharpe_ratio']:.2f}")

        elif args.command == "export":
            console.print(
                f"[bold cyan]Exporting {args.ticker.upper()} data to {args.format.upper()}...[/bold cyan]"
            )
            path = export(args.ticker, format=args.format, path=args.path, period=args.period)
            console.print(
                f"[bold green]SUCCESS:[/bold green] Exported to [underline]{path}[/underline]"
            )

    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
