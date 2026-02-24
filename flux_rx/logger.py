# Flux-RX Logging Module
from __future__ import annotations

import logging
from rich.logging import RichHandler
from rich.console import Console

# Create a single global console for the application
console = Console()


def get_logger(name: str) -> logging.Logger:
    """
    Get a pre-configured structured logger.

    Args:
        name: Name of the logger, typically __name__.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # Use RichHandler to format logs beautifully in the terminal
        handler = RichHandler(
            console=console, rich_tracebacks=True, show_time=False, show_path=False, markup=True
        )
        logger.addHandler(handler)

    return logger
