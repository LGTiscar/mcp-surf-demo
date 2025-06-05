#!/usr/bin/env python3
"""
Simple test to isolate the Gemini integration issue
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai


async def test_gemini_simple():
    """Test Gemini without MCP tools first."""
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    print("🤖 Testing simple Gemini response...")
    response = model.generate_content("What is 2 + 2?")
    print("📝 Response:", response.text)
    
    print("\n🔧 Testing function calling setup...")
    
    # Create a simple function declaration
    tools = [{
        "name": "test_function",
        "description": "A test function",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "A test message"}
            },
            "required": ["message"]
        }
    }]
    
    chat = model.start_chat(enable_automatic_function_calling=False)
    
    try:
        response = chat.send_message(
            "Call the test_function with message 'hello'",
            tools=tools
        )
        
        print("Response candidates:", len(response.candidates))
        if response.candidates:
            print("Parts:", len(response.candidates[0].content.parts))
            for i, part in enumerate(response.candidates[0].content.parts):
                print(f"Part {i} type:", type(part))
                print(f"Part {i} attributes:", [attr for attr in dir(part) if not attr.startswith('_')])
                if hasattr(part, 'function_call'):
                    print(f"Function call found: {part.function_call}")
                if hasattr(part, 'text'):
                    print(f"Text found: {part.text}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gemini_simple())
