#!/usr/bin/env python3
"""
Test script to understand Fetch-Browser MCP server capabilities
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_fetch_browser():
    """Test the Fetch-Browser MCP server to understand its tools."""
    
    # Path to the built Fetch-Browser server
    server_params = StdioServerParameters(
        command="node",
        args=["/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                print(f"Available tools: {len(tools_response.tools)}")
                
                for tool in tools_response.tools:
                    print(f"\nTool: {tool.name}")
                    print(f"Description: {tool.description}")
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        print(f"Input Schema: {json.dumps(tool.inputSchema, indent=2)}")
                
                # Test a simple fetch
                print("\n" + "="*50)
                print("Testing fetch_url tool...")
                
                result = await session.call_tool(
                    "fetch_url", 
                    {
                        "url": "https://httpbin.org/json",
                        "responseType": "text"
                    }
                )
                
                print("Fetch result:")
                print(json.dumps(result.content, indent=2))
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_fetch_browser())
