#!/usr/bin/env python3
"""
Basic MCP Demo - Test the Fetch-Browser MCP server directly without Gemini.

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
    """A basic demo that uses Fetch-Browser MCP directly without AI."""
    
    def __init__(self):
        self.console = Console()
        self.available_tools: List[Any] = []
        load_dotenv()
    
    def _prepare_env(self) -> Dict[str, str]:
        """Prepare environment variables for MCP server."""
        # Fetch-Browser doesn't require API keys, just return the base environment
        return os.environ.copy()
    
    async def connect_to_mcp(self) -> bool:
        """Connect to the Fetch-Browser MCP server."""
        try:
            self.console.print("[yellow]🔌 Connecting to Fetch-Browser MCP server...[/yellow]")
            
            env = self._prepare_env()
            
            # Start MCP server
            server_params = StdioServerParameters(
                command="node",
                args=["/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js"],
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
        
        server_params = StdioServerParameters(
            command="node",
            args=["/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js"],
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
            "This demo will show you how to use Fetch-Browser MCP tools for web automation.",
            title="Demo",
            border_style="cyan"
        ))
        
        try:
            # Step 1: Search Google
            query = "Python MCP servers"
            self.console.print(f"\n[cyan]🔍 Step 1: Searching Google for '{query}'[/cyan]")
            
            result = await self.call_tool("google_search", {
                "query": query,
                "maxResults": 5,
                "responseType": "text"
            })
            
            if hasattr(result, 'content') and result.content:
                content_text = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        content_text += content.text
                
                # Show first 300 characters
                preview = content_text[:300] + "..." if len(content_text) > 300 else content_text
                self.console.print(f"[green]✅ Search results retrieved![/green]")
                self.console.print(f"[dim]Preview: {preview}[/dim]")
            
            # Step 2: Fetch a specific webpage
            url = "https://httpbin.org/json"
            self.console.print(f"\n[cyan]📄 Step 2: Fetching content from {url}[/cyan]")
            
            result = await self.call_tool("fetch_url", {
                "url": url,
                "responseType": "text"
            })
            
            if hasattr(result, 'content') and result.content:
                content_text = ""
                for content in result.content:
                    if hasattr(content, 'text'):
                        content_text += content.text
                
                self.console.print(f"[green]✅ Content fetched![/green]")
                self.console.print(f"[dim]Content: {content_text}[/dim]")
            
            self.console.print(f"\n[green]🎉 Demo completed successfully![/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Demo failed: {e}[/red]")
    
    async def interactive_mode(self):
        """Interactive mode for manual tool testing."""
        self.console.print(Panel(
            "[bold cyan]🎮 Interactive Fetch-Browser Tool Testing[/bold cyan]\n\n"
            "You can now test Fetch-Browser MCP tools manually. Available commands:\n"
            "• search <query> - Search Google for a query\n"
            "• fetch <url> - Fetch content from a URL\n"
            "• news <query> - Search for news about a topic\n"
            "• quit - Exit interactive mode",
            title="Interactive Mode",
            border_style="cyan"
        ))
        
        while True:
            try:
                command = Prompt.ask("\n[bold green]Enter command[/bold green]", default="quit").strip()
                
                if command.lower() == "quit":
                    break
                elif command.lower().startswith("search "):
                    query = command[7:].strip()
                    if query:
                        result = await self.call_tool("google_search", {
                            "query": query,
                            "maxResults": 5,
                            "responseType": "text"
                        })
                        self.console.print(f"[green]✅ Search completed for '{query}'[/green]")
                        if hasattr(result, 'content') and result.content:
                            for content in result.content:
                                if hasattr(content, 'text'):
                                    preview = content.text[:500] + "..." if len(content.text) > 500 else content.text
                                    self.console.print(f"[dim]{preview}[/dim]")
                    else:
                        self.console.print("[red]❌ Please provide a search query[/red]")
                elif command.lower().startswith("fetch "):
                    url = command[6:].strip()
                    if url:
                        result = await self.call_tool("fetch_url", {
                            "url": url,
                            "responseType": "text"
                        })
                        self.console.print(f"[green]✅ Content fetched from {url}[/green]")
                        if hasattr(result, 'content') and result.content:
                            for content in result.content:
                                if hasattr(content, 'text'):
                                    preview = content.text[:500] + "..." if len(content.text) > 500 else content.text
                                    self.console.print(f"[dim]{preview}[/dim]")
                    else:
                        self.console.print("[red]❌ Please provide a URL[/red]")
                elif command.lower().startswith("news "):
                    query = command[5:].strip()
                    if query:
                        result = await self.call_tool("google_search", {
                            "query": query,
                            "topic": "news",
                            "maxResults": 5,
                            "responseType": "text"
                        })
                        self.console.print(f"[green]✅ News search completed for '{query}'[/green]")
                        if hasattr(result, 'content') and result.content:
                            for content in result.content:
                                if hasattr(content, 'text'):
                                    preview = content.text[:500] + "..." if len(content.text) > 500 else content.text
                                    self.console.print(f"[dim]{preview}[/dim]")
                    else:
                        self.console.print("[red]❌ Please provide a search query[/red]")
                else:
                    self.console.print("[yellow]❓ Unknown command. Try: search <query>, fetch <url>, news <query>, or quit[/yellow]")
                    
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
        "This demo shows how to use the Fetch-Browser MCP server directly\n"
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
        console.print("1. Run automated demo (Google search & URL fetch)")
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
