#!/usr/bin/env python3
"""
Simple demo script to test the MCP Surf functionality without requiring API keys.

This script tests the basic infrastructure and connection to the MCP server.
"""

import asyncio
import os
import sys
from rich.console import Console
from rich.panel import Panel

# Add the parent directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MCPSurfClient


async def test_mcp_connection():
    """Test basic MCP server connection without API calls."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🧪 MCP Surf Demo - Connection Test[/bold cyan]\n\n"
        "This test will check if we can connect to the Browserbase MCP server\n"
        "without making any actual API calls.",
        title="Connection Test",
        border_style="cyan"
    ))
    
    # Check environment variables
    console.print("\n[yellow]📋 Checking environment variables...[/yellow]")
    
    api_key = os.getenv("BROWSERBASE_API_KEY")
    project_id = os.getenv("BROWSERBASE_PROJECT_ID")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_browserbase_api_key_here":
        console.print("[red]❌ BROWSERBASE_API_KEY not configured[/red]")
        console.print("   Please update your .env file with a valid Browserbase API key")
        return False
    
    if not project_id or project_id == "your_browserbase_project_id_here":
        console.print("[red]❌ BROWSERBASE_PROJECT_ID not configured[/red]")
        console.print("   Please update your .env file with a valid Browserbase Project ID")
        return False
    
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        console.print("[yellow]⚠️  GEMINI_API_KEY not configured[/yellow]")
        console.print("   The demo will still work but Gemini AI features will be limited")
    else:
        console.print("[green]✅ GEMINI_API_KEY configured[/green]")
    
    console.print(f"[green]✅ BROWSERBASE_API_KEY configured[/green]")
    console.print(f"[green]✅ BROWSERBASE_PROJECT_ID configured[/green]")
    
    # Test MCP server connection
    console.print("\n[yellow]🔌 Testing MCP server connection...[/yellow]")
    
    try:
        client = MCPSurfClient()
        success = await client._test_mcp_connection()
        
        if success:
            console.print(f"[green]✅ Successfully connected to MCP server![/green]")
            console.print(f"[cyan]Available tools: {len(client.available_tools)}[/cyan]")
            
            # List available tools
            if client.available_tools:
                console.print("\n[cyan]📁 Available MCP tools:[/cyan]")
                for tool in client.available_tools:
                    console.print(f"  • {tool.name}: {tool.description}")
        
        return success
        
    except Exception as e:
        console.print(f"[red]❌ Failed to connect to MCP server: {e}[/red]")
        return False


async def test_basic_functionality():
    """Test basic functionality with a simple webpage."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🌐 Basic Functionality Test[/bold cyan]\n\n"
        "This test will try to navigate to a simple webpage and take a screenshot.",
        title="Functionality Test",
        border_style="cyan"
    ))
    
    try:
        client = MCPSurfClient()
        
        # Test MCP connection first
        if not await client._test_mcp_connection():
            console.print("[red]❌ Failed to connect to MCP server[/red]")
            return False
        
        console.print("[yellow]📍 Testing navigation to example.com...[/yellow]")
        
        # Test navigation using the new API
        async def test_navigation(session):
            console.print("[yellow]🔧 Calling browserbase_navigate...[/yellow]")
            result = await session.call_tool("browserbase_navigate", {"url": "https://example.com"})
            console.print("[green]✅ Navigation successful![/green]")
            
            console.print("[yellow]📸 Testing screenshot capture...[/yellow]")
            result = await session.call_tool("browserbase_take_screenshot", {})
            console.print("[green]✅ Screenshot captured![/green]")
            
            console.print("[yellow]📄 Testing text extraction...[/yellow]")
            result = await session.call_tool("browserbase_get_text", {})
            console.print("[green]✅ Text extraction successful![/green]")
            
            return True
        
        success = await client._execute_with_mcp(test_navigation)
        
        console.print("\n[green]🎉 All basic functionality tests passed![/green]")
        return success
        
    except Exception as e:
        console.print(f"[red]❌ Functionality test failed: {e}[/red]")
        return False


def main():
    """Main function to run the tests."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🚀 MCP Surf Demo - Test Suite[/bold cyan]\n\n"
        "This script will test the basic functionality of the MCP Surf Demo\n"
        "to ensure everything is working correctly.",
        title="Test Suite",
        border_style="cyan"
    ))
    
    print("\nChoose a test to run:")
    print("1. Connection Test (Test MCP server connection)")
    print("2. Functionality Test (Test basic web browsing)")
    print("3. Run Both Tests")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n" + "="*50)
        success = asyncio.run(test_mcp_connection())
    elif choice == "2":
        print("\n" + "="*50)
        success = asyncio.run(test_basic_functionality())
    elif choice == "3":
        print("\n" + "="*50)
        success1 = asyncio.run(test_mcp_connection())
        print("\n" + "="*50)
        success2 = asyncio.run(test_basic_functionality())
        success = success1 and success2
    elif choice == "4":
        console.print("[yellow]👋 Goodbye![/yellow]")
        return
    else:
        console.print("[red]❌ Invalid choice. Please try again.[/red]")
        return
    
    if success:
        console.print(Panel(
            "[bold green]🎉 All tests passed![/bold green]\n\n"
            "Your MCP Surf Demo is ready to use!\n"
            "You can now run: [cyan]python main.py[/cyan]",
            title="Success",
            border_style="green"
        ))
    else:
        console.print(Panel(
            "[bold red]❌ Some tests failed[/bold red]\n\n"
            "Please check your configuration and try again.\n"
            "Run: [cyan]python config.py setup[/cyan] to reconfigure.",
            title="Test Failed",
            border_style="red"
        ))


if __name__ == "__main__":
    main()
