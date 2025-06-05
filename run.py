#!/usr/bin/env python3
"""
Simple launcher script for MCP Surf Demo.

This script provides an easy way to start either the main interactive demo
or the basic demo without needing to know which file to run.
"""

import asyncio
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


def main():
    """Main launcher function."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🚀 MCP Surf Demo Launcher[/bold cyan]\n\n"
        "Choose which demo you'd like to run:\n\n"
        "[bold green]1.[/bold green] Interactive Demo (Gemini AI + Web browsing)\n"
        "[bold green]2.[/bold green] Basic Demo (Direct MCP tool testing)\n"
        "[bold green]3.[/bold green] Run Integration Tests\n"
        "[bold green]4.[/bold green] Exit",
        title="Welcome",
        border_style="cyan"
    ))
    
    try:
        choice = Prompt.ask(
            "\n[bold green]Enter your choice[/bold green]", 
            choices=["1", "2", "3", "4"], 
            default="1"
        )
        
        if choice == "1":
            console.print("[yellow]🤖 Starting Interactive Demo with Gemini AI...[/yellow]")
            from main import main as run_main
            asyncio.run(run_main())
            
        elif choice == "2":
            console.print("[yellow]🔧 Starting Basic MCP Demo...[/yellow]")
            from basic_demo import main as run_basic
            asyncio.run(run_basic())
            
        elif choice == "3":
            console.print("[yellow]🧪 Running Integration Tests...[/yellow]")
            from test_integration import test_integration
            asyncio.run(test_integration())
            
        else:
            console.print("[yellow]👋 Goodbye![/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
