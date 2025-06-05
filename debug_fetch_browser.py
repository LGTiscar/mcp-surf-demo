#!/usr/bin/env python3
"""
Debug script to understand Fetch-Browser response format
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def debug_fetch_browser():
    """Debug the Fetch-Browser response format."""
    
    server_params = StdioServerParameters(
        command="node",
        args=["/Users/lgarciat-local/Dev/PERSONAL/fetch-browser/build/index.js"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("Testing fetch_url tool...")
                result = await session.call_tool(
                    "fetch_url", 
                    {
                        "url": "https://httpbin.org/json",
                        "responseType": "text"
                    }
                )
                
                print("Result type:", type(result))
                print("Result attributes:", dir(result))
                
                if hasattr(result, 'content'):
                    print("Content type:", type(result.content))
                    print("Content length:", len(result.content))
                    for i, content in enumerate(result.content):
                        print(f"Content[{i}] type:", type(content))
                        print(f"Content[{i}] attributes:", dir(content))
                        if hasattr(content, 'text'):
                            print(f"Content[{i}] text:", content.text[:200])
                        else:
                            print(f"Content[{i}] value:", content)
                
                print("\n" + "="*50)
                print("Testing google_search tool...")
                result2 = await session.call_tool(
                    "google_search", 
                    {
                        "query": "Python",
                        "maxResults": 2,
                        "responseType": "text"
                    }
                )
                
                print("Result2 type:", type(result2))
                if hasattr(result2, 'content'):
                    print("Content2 length:", len(result2.content))
                    for i, content in enumerate(result2.content):
                        print(f"Content2[{i}] type:", type(content))
                        if hasattr(content, 'text'):
                            print(f"Content2[{i}] text:", content.text[:200])
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_fetch_browser())
