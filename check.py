#!/usr/bin/env python3
"""
System status checker for MCP Surf Demo.

This script checks if all required components are properly configured and available.
"""

import asyncio
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


async def check_system_status():
    """Check the status of all system components."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🔧 MCP Surf Demo - System Status Check[/bold cyan]\n\n"
        "Checking all required components...",
        title="System Check",
        border_style="cyan"
    ))
    
    # Load environment variables
    load_dotenv()
    
    # Create status table
    table = Table(title="System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="dim")
    
    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_status = "✅ OK" if sys.version_info >= (3, 11) else "❌ FAIL"
    table.add_row("Python Version", python_status, f"v{python_version} (requires 3.11+)")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_version = result.stdout.strip()
        node_status = "✅ OK" if result.returncode == 0 else "❌ FAIL"
        table.add_row("Node.js", node_status, node_version if node_status == "✅ OK" else "Not found")
    except FileNotFoundError:
        table.add_row("Node.js", "❌ FAIL", "Not installed")
    
    # Check Fetch-Browser MCP Server
    fetch_browser_path = Path("/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js")
    if fetch_browser_path.exists():
        table.add_row("Fetch-Browser MCP", "✅ OK", str(fetch_browser_path))
    else:
        table.add_row("Fetch-Browser MCP", "❌ FAIL", "Server not built")
    
    # Check environment variables
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and len(gemini_key) > 20:
        table.add_row("Gemini API Key", "✅ OK", f"Set (length: {len(gemini_key)})")
    else:
        table.add_row("Gemini API Key", "❌ FAIL", "Not set or invalid")
    
    # Check required Python packages
    required_packages = [
        ("mcp", "mcp"),
        ("google-generativeai", "google.generativeai"),
        ("rich", "rich"),
        ("python-dotenv", "dotenv")
    ]
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            table.add_row(f"Package: {package_name}", "✅ OK", "Installed")
        except ImportError:
            table.add_row(f"Package: {package_name}", "❌ FAIL", "Not installed")
    
    console.print(table)
    
    # Test MCP connection
    console.print("\n[yellow]🔌 Testing MCP connection...[/yellow]")
    try:
        from main import MCPSurfClient
        client = MCPSurfClient()
        if await client._test_mcp_connection():
            console.print("[green]✅ MCP connection test passed![/green]")
            return True
        else:
            console.print("[red]❌ MCP connection test failed[/red]")
            return False
    except Exception as e:
        console.print(f"[red]❌ MCP connection test error: {e}[/red]")
        return False


def main():
    """Main function."""
    console = Console()
    
    try:
        success = asyncio.run(check_system_status())
        
        if success:
            console.print(Panel(
                "[bold green]🎉 System Check Complete![/bold green]\n\n"
                "All components are properly configured. You can now run:\n"
                "• [cyan]python run.py[/cyan] - Launch the demo launcher\n"
                "• [cyan]python main.py[/cyan] - Interactive demo with Gemini\n"
                "• [cyan]python basic_demo.py[/cyan] - Basic MCP demo",
                title="Success",
                border_style="green"
            ))
        else:
            console.print(Panel(
                "[bold red]⚠️  System Check Failed[/bold red]\n\n"
                "Some components are not properly configured.\n"
                "Please check the failed items above and fix them before running the demo.",
                title="Attention Required",
                border_style="red"
            ))
            
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ System check failed: {e}[/red]")


if __name__ == "__main__":
    main()
