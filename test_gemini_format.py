#!/usr/bin/env python3
"""
Test Gemini function calling with correct format
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai


async def test_gemini_function_calling():
    """Test Gemini function calling with proper format."""
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Create tools in the correct format for Gemini
    tools = [
        genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="fetch_url",
                    description="Fetch content from a URL",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "url": genai.protos.Schema(type=genai.protos.Type.STRING),
                            "responseType": genai.protos.Schema(type=genai.protos.Type.STRING)
                        },
                        required=["url"]
                    )
                )
            ]
        )
    ]
    
    chat = model.start_chat(enable_automatic_function_calling=False)
    
    try:
        response = chat.send_message(
            "Fetch content from https://httpbin.org/json",
            tools=tools
        )
        
        print("✅ Function calling setup works!")
        print("Response candidates:", len(response.candidates))
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call'):
                    print(f"Function call: {part.function_call.name}")
                    print(f"Arguments: {dict(part.function_call.args)}")
                elif hasattr(part, 'text'):
                    print(f"Text: {part.text}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gemini_function_calling())
