#!/usr/bin/env python3
"""
Example usage of the MCP Surf Demo client.

This script demonstrates specific use cases for web browsing with Gemini + Browserbase.
"""

import asyncio
import sys
from main import MCPSurfClient


async def example_website_analysis():
    """Example: Analyze a website and extract key information."""
    client = MCPSurfClient()
    
    try:
        print("🚀 Starting MCP server...")
        await client.start_mcp_server()
        
        print("\n📊 Analyzing a website...")
        response = await client.chat(
            "Please navigate to https://news.ycombinator.com and tell me what the top 3 stories are today. "
            "Extract the titles and provide a brief summary of what types of topics are trending."
        )
        print(f"\n🤖 Analysis Result:\n{response}")
        
        print("\n📸 Taking a screenshot...")
        response = await client.chat(
            "Please take a screenshot of the current page to capture the content we just analyzed."
        )
        print(f"\n📷 Screenshot Result:\n{response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.cleanup()


async def example_search_and_extract():
    """Example: Search for information and extract specific data."""
    client = MCPSurfClient()
    
    try:
        print("🚀 Starting MCP server...")
        await client.start_mcp_server()
        
        print("\n🔍 Searching for Python MCP information...")
        response = await client.chat(
            "Please navigate to Google, search for 'Model Context Protocol Python', "
            "and tell me what the top 3 search results are. Extract the titles and URLs."
        )
        print(f"\n🤖 Search Result:\n{response}")
        
        print("\n📚 Getting more details...")
        response = await client.chat(
            "Now click on the first search result and summarize what the page is about. "
            "Focus on what MCP is and how it's used in Python applications."
        )
        print(f"\n📖 Summary:\n{response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.cleanup()


async def example_e_commerce_analysis():
    """Example: Analyze an e-commerce site."""
    client = MCPSurfClient()
    
    try:
        print("🚀 Starting MCP server...")
        await client.start_mcp_server()
        
        print("\n🛒 Analyzing an e-commerce site...")
        response = await client.chat(
            "Please navigate to https://example-shop.com (or any popular e-commerce site you can access) "
            "and analyze the homepage. Tell me about:\n"
            "1. What products are featured\n"
            "2. Any current promotions or deals\n"
            "3. The overall design and user experience\n"
            "4. Navigation structure"
        )
        print(f"\n🤖 E-commerce Analysis:\n{response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.cleanup()


def main():
    """Main function to run examples."""
    print("🌐 MCP Surf Demo - Example Usage\n")
    
    examples = {
        "1": ("Website Analysis (Hacker News)", example_website_analysis),
        "2": ("Search and Extract", example_search_and_extract),
        "3": ("E-commerce Analysis", example_e_commerce_analysis),
    }
    
    print("Available examples:")
    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")
    
    choice = input("\nEnter your choice (1-3) or 'q' to quit: ").strip()
    
    if choice.lower() == 'q':
        print("👋 Goodbye!")
        return
    
    if choice in examples:
        _, example_func = examples[choice]
        print(f"\n🎬 Running example: {examples[choice][0]}")
        asyncio.run(example_func())
    else:
        print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
