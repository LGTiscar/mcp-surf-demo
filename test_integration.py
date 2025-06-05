#!/usr/bin/env python3
"""
Quick test script to validate Fetch-Browser integration
"""

import asyncio
import os
from dotenv import load_dotenv
from main import MCPSurfClient


async def test_integration():
    """Test the Fetch-Browser integration with a simple query."""
    # Load environment
    load_dotenv()
    
    # Check if we have the required API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found. Please set it in your .env file")
        return
    
    print("🧪 Testing Fetch-Browser integration...")
    
    client = MCPSurfClient()
    
    # Test MCP connection
    if not await client._test_mcp_connection():
        print("❌ Failed to connect to Fetch-Browser MCP server")
        return
    
    print("✅ Fetch-Browser MCP server connected successfully!")
    print("✅ Available tools:", [tool.name for tool in client.available_tools])
    
    # Test a simple chat message
    print("\n🤖 Testing Gemini + Fetch-Browser integration...")
    response = await client.chat("Fetch content from https://httpbin.org/json and tell me what it contains")
    
    print("📝 Response:")
    print(response)
    
    print("\n🎉 Integration test completed!")


if __name__ == "__main__":
    asyncio.run(test_integration())
