#!/usr/bin/env python3
"""
Simple Gemini + MCP integration test - just tests basic function calling without overusing the quota
"""

import asyncio
from main import MCPSurfClient

async def test_simple_chat():
    """Test a simple chat interaction"""
    client = MCPSurfClient()
    
    try:
        # Test MCP connection first
        if not await client._test_mcp_connection():
            print("❌ MCP connection failed")
            return False
        
        print("\n🤖 Testing simple Gemini chat (without function calls)...")
        
        # Simple message that shouldn't trigger function calls
        response = await client.chat("Hello! Just say hello back without using any tools.")
        print(f"✅ Gemini response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_chat())
    if success:
        print("\n🎉 Simple integration test passed!")
    else:
        print("\n❌ Integration test failed")
