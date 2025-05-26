# Getting Started with MCP Surf Demo

Welcome to MCP Surf Demo! This guide will help you set up and start using the Python client that connects Gemini AI with web browsing capabilities via Browserbase.

## 🎯 What This Does

The MCP Surf Demo allows you to:
- Chat with Google's Gemini AI 
- Give Gemini the ability to browse websites
- Take screenshots of web pages
- Extract information from websites
- Interact with web pages (click, type, navigate)

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.11+** (you already have this if you're here!)
2. **Node.js** (for the Browserbase MCP server)
3. **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
4. **Browserbase Account** ([Sign up here](https://www.browserbase.com/))

## 🚀 Quick Setup

### Step 1: Install Dependencies
Dependencies are already installed if you used `uv sync`.

### Step 2: Configure Your Environment
Run the setup wizard:
```bash
python config.py setup
```

This will:
- Create a `.env` file for your API keys
- Guide you through getting the necessary API keys
- Test your configuration

### Step 3: Get Your API Keys

#### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

#### Browserbase API Key & Project ID
1. Go to [Browserbase](https://www.browserbase.com/)
2. Sign up for a free account
3. Go to your dashboard
4. Copy your API Key and Project ID

### Step 4: Update Your .env File
Edit the `.env` file and replace the placeholder values:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
BROWSERBASE_API_KEY=your_actual_browserbase_api_key_here
BROWSERBASE_PROJECT_ID=your_actual_browserbase_project_id_here
```

### Step 5: Test Your Setup
Run the test suite to make sure everything works:
```bash
python test.py
```

Choose option 3 to run both tests.

## 🎮 How to Use

### Interactive Mode
Start the interactive chat:
```bash
python main.py
```

Then try commands like:
- "Browse to https://news.ycombinator.com and tell me the top stories"
- "Take a screenshot of the current page"
- "Navigate to Google and search for 'Python MCP'"
- "Extract all the links from this page"

### Example Scripts
Run pre-built examples:
```bash
python examples.py
```

## 💡 Example Use Cases

1. **Website Analysis**: "Browse to reddit.com and summarize what's trending in technology"

2. **Research**: "Go to Wikipedia, search for 'Machine Learning', and give me a summary of the main concepts"

3. **E-commerce**: "Browse to amazon.com, search for 'laptop', and show me the top 3 results with prices"

4. **News Monitoring**: "Check the latest news on BBC.com and summarize the top 3 stories"

5. **Social Media**: "Go to Twitter.com and tell me what's trending today"

## 🔧 Troubleshooting

### Common Issues

**"MCP server failed to start"**
- Check that Node.js is installed: `node --version`
- Verify your Browserbase credentials are correct
- Make sure you have internet connectivity

**"Gemini API quota exceeded"**
- Check your Google AI Studio quota
- Verify your API key is correct
- Consider upgrading your plan if needed

**"Tool not found" errors**
- Restart the application
- Check that the MCP server started successfully
- Verify your Browserbase account is active

### Getting Help

1. Run `python config.py status` to check your configuration
2. Run `python test.py` to test your setup
3. Check the console output for detailed error messages

## 🎯 Next Steps

Once you have everything working:

1. **Explore the Examples**: Try `python examples.py` for inspiration
2. **Customize**: Modify the prompts and tools to fit your needs
3. **Integrate**: Use this as a foundation for your own projects

## 🔒 Security Notes

- Keep your API keys secure and never commit them to version control
- The `.env` file is gitignored by default
- Browserbase runs in isolated browser sessions for security

## 📚 Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Browserbase Documentation](https://docs.browserbase.com/)
- [Google Gemini API Documentation](https://ai.google.dev/)

---

**Happy browsing with AI! 🤖🌐**
