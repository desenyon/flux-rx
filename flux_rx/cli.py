# Flux-RX CLI Module: Command-line interface
from __future__ import annotations

import argparse
import sys
import os
from flux_rx import __version__, quick, metrics, info, chart, app


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
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    try:
        if args.command == "report":
            print(f"Generating report for {args.ticker}...")
            save_path = args.save or f"{args.ticker}_report.html"
            quick(
                args.ticker,
                period=args.period,
                benchmark=args.benchmark,
                theme=args.theme,
                save=save_path,
                show=not args.no_show
            )
            print(f"Report saved to {os.path.abspath(save_path)}")
            
        elif args.command == "metrics":
            data = metrics(
                args.ticker,
                period=args.period,
                benchmark=args.benchmark,
                formatted=not args.raw
            )
            print(f"\nMetrics for {args.ticker.upper()} ({args.period}):")
            print("-" * 40)
            for k, v in data.items():
                print(f"{k.replace('_', ' ').title():<20} {v}")
                
        elif args.command == "info":
            data = info(args.ticker)
            print(f"\nInfo for {args.ticker.upper()}:")
            print("-" * 40)
            for k, v in data.items():
                if k != "description":
                    print(f"{k.replace('_', ' ').title():<20} {v}")
            if data.get("description"):
                print("\nDescription:")
                print(data["description"][:500] + "..." if len(data["description"]) > 500 else data["description"])
                
        elif args.command == "dashboard":
            print(f"Launching dashboard on port {args.port}...")
            app(port=args.port, debug=args.debug)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
