# MCP Surf Demo

A Python client that connects to Google's Gemini AI and uses the Model Context Protocol (MCP) to browse and analyze webpages via Browserbase.

## Features

- 🤖 Integration with Google Gemini AI
- 🌐 Web browsing capabilities via Browserbase MCP server
- 📸 Screenshot capture and analysis
- 🔍 Intelligent webpage analysis and data extraction
- 💬 Interactive chat interface with web browsing capabilities

## Prerequisites

1. **Google Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Browserbase Account**: Sign up at [Browserbase](https://www.browserbase.com/) to get:
   - API Key
   - Project ID

## Setup

1. **Clone and install dependencies:**
```bash
# Install dependencies
uv sync
```

2. **Environment Configuration:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
```

3. **Configure your .env file:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
BROWSERBASE_API_KEY=your_browserbase_api_key_here
BROWSERBASE_PROJECT_ID=your_browserbase_project_id_here
BROWSERBASE_CONTEXT_ID=your_context_id_here  # Optional
```

## Usage

### Basic Usage

```bash
# Run the interactive demo
python main.py
```

### Example Interactions

- "Browse to https://example.com and tell me what you see"
- "Take a screenshot of the current page"
- "Extract all the links from this webpage"
- "Navigate to Google and search for 'Python MCP'"

## How It Works

1. **MCP Integration**: The client starts a Browserbase MCP server as a subprocess
2. **Gemini Connection**: Connects to Google's Gemini AI model
3. **Tool Usage**: Gemini can use browser tools to:
   - Navigate to URLs
   - Take screenshots
   - Extract text and data
   - Interact with page elements
4. **Intelligent Analysis**: Gemini analyzes the webpage content and provides insights

## Available Browser Tools

- `browserbase_navigate`: Navigate to any URL
- `browserbase_screenshot`: Take full-page screenshots
- `browserbase_get_text`: Extract text content from pages
- `browserbase_session_create`: Create new browser sessions
- `browserbase_context_create`: Create persistent contexts

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `BROWSERBASE_API_KEY`: Your Browserbase API key
- `BROWSERBASE_PROJECT_ID`: Your Browserbase project ID
- `BROWSERBASE_CONTEXT_ID`: (Optional) Browserbase context for persistent sessions

## Troubleshooting

1. **MCP Server Issues**: Ensure you have Node.js installed and the Browserbase MCP package available
2. **API Key Issues**: Verify your API keys are correctly set in the .env file
3. **Network Issues**: Check your internet connection and firewall settings

## Learn More

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Browserbase Documentation](https://docs.browserbase.com/)
- [Google Gemini API](https://ai.google.dev/)