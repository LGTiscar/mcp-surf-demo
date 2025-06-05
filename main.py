#!/usr/bin/env python3
"""
MCP Surf Demo - A Python client that connects to Gemini and uses MCP to browse webpages via Browserbase.

This is a fixed version that properly handles the MCP connection lifecycle.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPSurfClient:
    """A client that integrates Gemini AI with Fetch-Browser MCP for web browsing."""
    
    def __init__(self):
        """Initialize the MCP Surf Client."""
        self.console = Console()
        self.available_tools: List[Any] = []
        
        # Load environment variables
        load_dotenv()
        self._setup_gemini()
    
    def _setup_gemini(self) -> None:
        """Configure Google Gemini AI."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.console.print("[red]❌ GEMINI_API_KEY not found in environment variables[/red]")
            self.console.print("Please set your Gemini API key in the .env file")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def _prepare_env(self) -> Dict[str, str]:
        """Prepare environment variables for MCP server."""
        # Fetch-Browser doesn't require API keys, just return the base environment
        return os.environ.copy()
    
    async def _test_mcp_connection(self) -> bool:
        """Test MCP server connection and get available tools."""
        try:
            self.console.print("[yellow]🚀 Testing Fetch-Browser MCP server connection...[/yellow]")
            
            env = self._prepare_env()
            server_params = StdioServerParameters(
                command="node",
                args=["/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js"],
                env=env
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Get available tools
                    tools_response = await session.list_tools()
                    self.available_tools = tools_response.tools
                    
                    self.console.print(f"[green]✅ MCP server connected with {len(self.available_tools)} tools available[/green]")
                    
                    # Display available tools
                    tool_names = [tool.name for tool in self.available_tools]
                    self.console.print(f"[cyan]Available tools: {', '.join(tool_names)}[/cyan]")
                    
                    return True
                    
        except Exception as e:
            self.console.print(f"[red]❌ Failed to connect to MCP server: {e}[/red]")
            return False
    
    async def _execute_with_mcp(self, func) -> Any:
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
    
    async def call_tool(self, session: ClientSession, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool and return the result."""
        try:
            self.console.print(f"[yellow]🔧 Calling tool: {tool_name}[/yellow]")
            result = await session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            self.console.print(f"[red]❌ Error calling tool {tool_name}: {e}[/red]")
            raise
    
    def create_tool_functions_for_gemini(self) -> List[Any]:
        """Convert MCP tools to Gemini function calling format."""
        tools = []
        
        for tool in self.available_tools:
            if tool.name == "fetch_url":
                function_declaration = genai.protos.FunctionDeclaration(
                    name="fetch_url",
                    description="Fetch content from a URL with proper error handling and response processing",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "url": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="The URL to fetch"
                            ),
                            "responseType": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Expected response type: text, json, html, markdown"
                            ),
                            "timeout": genai.protos.Schema(
                                type=genai.protos.Type.NUMBER,
                                description="Request timeout in milliseconds"
                            )
                        },
                        required=["url"]
                    )
                )
            elif tool.name == "google_search":
                function_declaration = genai.protos.FunctionDeclaration(
                    name="google_search",
                    description="Execute a Google search and return results in various formats",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "query": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="The search query to execute"
                            ),
                            "responseType": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Expected response type: text, json, html, markdown"
                            ),
                            "maxResults": genai.protos.Schema(
                                type=genai.protos.Type.NUMBER,
                                description="Maximum number of results to return"
                            ),
                            "topic": genai.protos.Schema(
                                type=genai.protos.Type.STRING,
                                description="Type of search to perform: web or news"
                            )
                        },
                        required=["query"]
                    )
                )
            else:
                continue  # Skip unknown tools
            
            tools.append(genai.protos.Tool(function_declarations=[function_declaration]))
        
        return tools
    
    async def handle_function_call(self, session: ClientSession, function_call) -> str:
        """Handle a function call from Gemini."""
        function_name = function_call.name
        function_args = dict(function_call.args) if function_call.args else {}
        
        try:
            # Call the MCP tool
            result = await self.call_tool(session, function_name, function_args)
            
            # Format the result for Gemini
            if hasattr(result, 'content') and result.content:
                # Handle text content
                content_parts = []
                for content in result.content:
                    if hasattr(content, 'text'):
                        content_parts.append(content.text)
                    elif hasattr(content, 'data') and hasattr(content, 'mimeType'):
                        # Handle binary data (like images)
                        if content.mimeType.startswith('image/'):
                            # For images, we'll describe them since we can't directly display
                            content_parts.append(f"[Image captured: {content.mimeType}]")
                        else:
                            content_parts.append(f"[Binary data: {content.mimeType}]")
                    else:
                        # For simple string content
                        content_parts.append(str(content))
                
                return "\n".join(content_parts) if content_parts else "Tool executed successfully"
            elif result:
                # If result is not None but doesn't have content, convert to string
                return str(result)
            else:
                return "Tool executed successfully"
                
        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"
    
    async def chat(self, message: str) -> str:
        """Send a message to Gemini with access to MCP tools."""
        async def _chat_with_session(session: ClientSession) -> str:
            try:
                # Create Gemini tools from MCP tools
                tools = self.create_tool_functions_for_gemini()
                
                # Create a chat session with tools
                chat = self.model.start_chat(
                    enable_automatic_function_calling=False  # We'll handle function calls manually
                )
                
                # Send the message
                response = chat.send_message(
                    message,
                    tools=tools
                )
                
                # Handle function calls if any
                if response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            # Execute the function call
                            function_result = await self.handle_function_call(session, part.function_call)
                            
                            # Send the result back to Gemini
                            response = chat.send_message([
                                {
                                    "function_response": {
                                        "name": part.function_call.name,
                                        "response": {"result": function_result}
                                    }
                                }
                            ])
                
                return response.text
                
            except Exception as e:
                return f"Error processing message: {str(e)}"
        
        return await self._execute_with_mcp(_chat_with_session)
    
    async def run_interactive(self) -> None:
        """Run an interactive chat session."""
        self.console.print(Panel(
            "[bold cyan]🌐 MCP Surf Demo - Gemini + Fetch-Browser[/bold cyan]\n\n"
            "Ask me to search Google, browse websites, or analyze web content!\n\n"
            "[dim]Examples:[/dim]\n"
            "• Search Google for 'Python MCP servers'\n"
            "• Fetch content from https://example.com and summarize it\n"
            "• Search for news about artificial intelligence\n"
            "• Get the latest information from a specific URL\n\n"
            "[dim]Type 'quit' to exit[/dim]",
            title="Welcome",
            border_style="cyan"
        ))
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[bold green]You[/bold green]", default="quit")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                
                # Process the message
                self.console.print("[yellow]🤖 Gemini is thinking...[/yellow]")
                response = await self.chat(user_input)
                
                # Display the response
                self.console.print(Panel(
                    Markdown(response),
                    title="[bold blue]Gemini[/bold blue]",
                    border_style="blue"
                ))
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"[red]❌ Error: {e}[/red]")


async def main():
    """Main entry point."""
    client = MCPSurfClient()
    
    try:
        # Test MCP server connection first
        if not await client._test_mcp_connection():
            client.console.print("[red]❌ Failed to connect to MCP server. Please check your configuration.[/red]")
            return
        
        # Run interactive session
        await client.run_interactive()
        
    except KeyboardInterrupt:
        client.console.print("\n[yellow]👋 Goodbye![/yellow]")
    except Exception as e:
        client.console.print(f"[red]❌ Fatal error: {e}[/red]")


if __name__ == "__main__":
    asyncio.run(main())
