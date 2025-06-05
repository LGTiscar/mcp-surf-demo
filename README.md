# MCP Surf Demo

A Python client that connects to Google's Gemini AI and uses the Model Context Protocol (MCP) to browse and analyze webpages via the open-source Fetch-Browser MCP server.

## Features

- 🤖 Integration with Google Gemini AI
- 🌐 Web browsing capabilities via Fetch-Browser MCP server
- 🔍 Google search functionality with result analysis
- 📄 URL content fetching and analysis
- 🆓 No API limits - uses open-source tools
- 💬 Interactive chat interface with web browsing capabilities

## Project Structure

```
mcp-surf-demo/
├── main.py              # Main application entry point
├── basic_demo.py        # Basic MCP demo without AI
├── run.py               # Simple launcher script
├── check.py             # System status checker
├── config.py            # Configuration helper and setup wizard
├── test_integration.py  # Integration test suite
├── tests/               # Test files
│   ├── __init__.py      # Test package initialization
│   ├── test.py          # Comprehensive test suite
│   └── simple_test.py   # Simple integration test
├── README.md            # This file
├── GETTING_STARTED.md   # Detailed setup guide
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment variables template
└── .gitignore           # Git ignore rules
```

## Prerequisites

1. **Google Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Fetch-Browser MCP Server**: This will be automatically installed during setup

## Setup

1. **Clone and install dependencies:**
```bash
# Install dependencies
uv sync

# Clone and build Fetch-Browser MCP server
git clone https://github.com/modelcontextprotocol/fetch-browser.git /Users/lgarciat-local/Dev/PERSONAL/fetch-browser
cd /Users/lgarciat-local/Dev/PERSONAL/fetch-browser
npm install
npm run build
```

2. **Environment Configuration:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Gemini API key only
# Note: Fetch-Browser doesn't require any API keys!
```

3. **Configure your .env file:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
# That's it! Fetch-Browser doesn't need any API keys
```

## Usage

### Quick Start with Launcher

```bash
# Check system configuration first
python check.py

# Use the launcher script for easy access to all demos
python run.py
```

The launcher provides options for:
1. Interactive Demo (Gemini AI + Web browsing)
2. Basic Demo (Direct MCP tool testing)
3. Integration Tests
4. Exit

### Direct Usage

```bash
# Run the interactive demo with Gemini AI
python main.py

# Run the basic MCP demo (no AI required)
python basic_demo.py

# Run integration tests
python test_integration.py
```

### Example Interactions

- "Search Google for 'Python MCP servers' and summarize the results"
- "Fetch content from https://example.com and tell me what you see"
- "Search for recent news about artificial intelligence"
- "Get the latest information about MCP protocol from the web"

## How It Works

1. **MCP Integration**: The client starts a Fetch-Browser MCP server as a subprocess
2. **Gemini Connection**: Connects to Google's Gemini AI model
3. **Tool Usage**: Gemini can use web browsing tools to:
   - Search Google for information
   - Fetch content from any URL
   - Search for news on specific topics
   - Process and analyze web content
4. **Intelligent Analysis**: Gemini analyzes the fetched content and provides insights

## Available Browser Tools

- `google_search`: Search Google with customizable parameters (query, maxResults, topic, responseType)
- `fetch_url`: Fetch content from any URL with error handling and multiple response formats

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