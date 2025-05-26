#!/usr/bin/env python3
"""
Basic MCP Demo - Test the Browserbase MCP server directly without Gemini.

This script demonstrates how to use the MCP server directly for web automation.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class BasicMCPDemo:
    """A basic demo that uses MCP directly without AI."""
    
    def __init__(self):
        self.console = Console()
        self.available_tools: List[Any] = []
        load_dotenv()
    
    def _prepare_env(self) -> Dict[str, str]:
        """Prepare environment variables for MCP server."""
        api_key = os.getenv("BROWSERBASE_API_KEY")
        project_id = os.getenv("BROWSERBASE_PROJECT_ID")
        
        if not api_key or api_key == "your_browserbase_api_key_here":
            self.console.print("[red]❌ BROWSERBASE_API_KEY not configured[/red]")
            return None
        
        if not project_id or project_id == "your_browserbase_project_id_here":
            self.console.print("[red]❌ BROWSERBASE_PROJECT_ID not configured[/red]")
            return None
        
        env = os.environ.copy()
        env.update({
            "BROWSERBASE_API_KEY": api_key,
            "BROWSERBASE_PROJECT_ID": project_id,
        })
        
        return env
    
    async def connect_to_mcp(self) -> bool:
        """Connect to the Browserbase MCP server."""
        try:
            self.console.print("[yellow]🔌 Connecting to Browserbase MCP server...[/yellow]")
            
            env = self._prepare_env()
            if not env:
                return False
            
            # Start MCP server
            server_params = StdioServerParameters(
                command="npx",
                args=["@browserbasehq/mcp"],
                env=env
            )
            
            # Test connection and get tools
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Get available tools
                    tools_response = await session.list_tools()
                    self.available_tools = tools_response.tools
                    
                    self.console.print(f"[green]✅ Connected! Found {len(self.available_tools)} tools[/green]")
                    
                    # Display available tools
                    if self.available_tools:
                        table = Table(title="Available MCP Tools")
                        table.add_column("Tool Name", style="cyan")
                        table.add_column("Description", style="green")
                        
                        for tool in self.available_tools:
                            table.add_row(tool.name, tool.description)
                        
                        self.console.print(table)
                    
                    return True
            
        except Exception as e:
            self.console.print(f"[red]❌ Failed to connect: {e}[/red]")
            return False
    
    async def _execute_with_mcp(self, func):
        """Execute a function with an active MCP connection."""
        env = self._prepare_env()
        if not env:
            raise RuntimeError("Environment not configured properly")
        
        server_params = StdioServerParameters(
            command="npx",
            args=["@browserbasehq/mcp"],
            env=env
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await func(session)
    
    async def call_tool(self, tool_name: str, arguments: dict) -> any:
        """Call an MCP tool and return the result."""
        async def _call_tool_with_session(session):
            self.console.print(f"[yellow]🔧 Calling {tool_name}...[/yellow]")
            result = await session.call_tool(tool_name, arguments)
            return result
        
        try:
            return await self._execute_with_mcp(_call_tool_with_session)
        except Exception as e:
            self.console.print(f"[red]❌ Error calling {tool_name}: {e}[/red]")
            raise
    
    async def demo_basic_browsing(self):
        """Demonstrate basic web browsing capabilities."""
        self.console.print(Panel(
            "[bold cyan]🌐 Basic Web Browsing Demo[/bold cyan]\n\n"
            "This demo will show you how to use MCP tools directly for web automation.",
            title="Demo",
            border_style="cyan"
        ))
        
        try:
            # Step 1: Navigate to a website
            url = "https://example.com"
            self.console.print(f"\n[cyan]📍 Step 1: Navigating to {url}[/cyan]")
            
            result = await self.call_tool("browserbase_navigate", {"url": url})
            self.console.print("[green]✅ Navigation successful![/green]")
            
            # Step 2: Take a screenshot
            self.console.print(f"\n[cyan]📸 Step 2: Taking a screenshot[/cyan]")
            
            result = await self.call_tool("browserbase_take_screenshot", {})
            self.console.print("[green]✅ Screenshot captured![/green]")
            
            # Step 3: Get page text
            self.console.print(f"\n[cyan]📄 Step 3: Extracting page text[/cyan]")
            
            result = await self.call_tool("browserbase_get_text", {})
            if hasattr(result, 'content') and result.content:
                content_text = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        content_text += content.text
                
                # Show first 200 characters
                preview = content_text[:200] + "..." if len(content_text) > 200 else content_text
                self.console.print(f"[green]✅ Text extracted![/green]")
                self.console.print(f"[dim]Preview: {preview}[/dim]")
            
            self.console.print(f"\n[green]🎉 Demo completed successfully![/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Demo failed: {e}[/red]")
    
    async def interactive_mode(self):
        """Interactive mode for manual tool testing."""
        self.console.print(Panel(
            "[bold cyan]🎮 Interactive MCP Tool Testing[/bold cyan]\n\n"
            "You can now test MCP tools manually. Available commands:\n"
            "• navigate <url> - Navigate to a URL\n"
            "• screenshot - Take a screenshot\n"
            "• text - Get page text\n"
            "• quit - Exit interactive mode",
            title="Interactive Mode",
            border_style="cyan"
        ))
        
        while True:
            try:
                command = Prompt.ask("\n[bold green]Enter command[/bold green]").strip().lower()
                
                if command == "quit":
                    break
                elif command.startswith("navigate "):
                    url = command[9:].strip()
                    if url:
                        await self.call_tool("browserbase_navigate", {"url": url})
                        self.console.print(f"[green]✅ Navigated to {url}[/green]")
                    else:
                        self.console.print("[red]❌ Please provide a URL[/red]")
                elif command == "screenshot":
                    await self.call_tool("browserbase_take_screenshot", {})
                    self.console.print("[green]✅ Screenshot taken[/green]")
                elif command == "text":
                    result = await self.call_tool("browserbase_get_text", {})
                    self.console.print("[green]✅ Text extracted[/green]")
                else:
                    self.console.print("[yellow]❓ Unknown command. Try: navigate <url>, screenshot, text, or quit[/yellow]")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"[red]❌ Error: {e}[/red]")
    
    async def cleanup(self):
        """Clean up resources."""
        # No persistent session to clean up in this fixed version
        self.console.print("[dim]Resources cleaned up[/dim]")


async def main():
    """Main function."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🚀 Basic MCP Demo[/bold cyan]\n\n"
        "This demo shows how to use the Browserbase MCP server directly\n"
        "without requiring Gemini AI. Perfect for testing your setup!",
        title="Welcome",
        border_style="cyan"
    ))
    
    demo = BasicMCPDemo()
    
    try:
        # Connect to MCP server
        if not await demo.connect_to_mcp():
            console.print("[red]❌ Failed to connect to MCP server. Please check your configuration.[/red]")
            return
        
        # Choose what to do
        console.print("\n[cyan]What would you like to do?[/cyan]")
        console.print("1. Run automated demo (navigate to example.com)")
        console.print("2. Interactive mode (manual tool testing)")
        console.print("3. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            await demo.demo_basic_browsing()
        elif choice == "2":
            await demo.interactive_mode()
        else:
            console.print("[yellow]👋 Goodbye![/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")
    finally:
        await demo.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
