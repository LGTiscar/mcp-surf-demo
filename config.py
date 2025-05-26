#!/usr/bin/env python3
"""
Configuration helper for MCP Surf Demo.

This script helps users set up their environment and test their API connections.
"""

import os
import sys
from pathlib import Path
from typing import Dict

import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table


class ConfigHelper:
    """Helper class for setting up the MCP Surf Demo configuration."""
    
    def __init__(self):
        self.console = Console()
        self.env_file = Path(".env")
        load_dotenv()
    
    def check_env_file(self) -> bool:
        """Check if .env file exists."""
        if not self.env_file.exists():
            self.console.print("[yellow]⚠️  .env file not found[/yellow]")
            if Confirm.ask("Would you like to create one from the example?"):
                self.create_env_from_example()
                return True
            return False
        return True
    
    def create_env_from_example(self) -> None:
        """Create .env file from .env.example."""
        example_file = Path(".env.example")
        if example_file.exists():
            content = example_file.read_text()
            self.env_file.write_text(content)
            self.console.print("[green]✅ Created .env file from example[/green]")
        else:
            # Create a basic .env file
            content = """# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Browserbase Configuration
BROWSERBASE_API_KEY=your_browserbase_api_key_here
BROWSERBASE_PROJECT_ID=your_browserbase_project_id_here

# Optional: Browserbase Context ID for persistent sessions
BROWSERBASE_CONTEXT_ID=your_context_id_here
"""
            self.env_file.write_text(content)
            self.console.print("[green]✅ Created basic .env file[/green]")
    
    def check_configuration(self) -> Dict[str, bool]:
        """Check the current configuration status."""
        status = {}
        
        # Check Gemini API key
        gemini_key = os.getenv("GEMINI_API_KEY")
        status["gemini"] = gemini_key is not None and gemini_key != "your_gemini_api_key_here"
        
        # Check Browserbase configuration
        browserbase_key = os.getenv("BROWSERBASE_API_KEY")
        browserbase_project = os.getenv("BROWSERBASE_PROJECT_ID")
        status["browserbase_key"] = browserbase_key is not None and browserbase_key != "your_browserbase_api_key_here"
        status["browserbase_project"] = browserbase_project is not None and browserbase_project != "your_browserbase_project_id_here"
        
        return status
    
    def test_gemini_connection(self) -> bool:
        """Test the Gemini API connection."""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key == "your_gemini_api_key_here":
                self.console.print("[red]❌ Gemini API key not configured[/red]")
                return False
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            # Test with a simple prompt
            response = model.generate_content("Hello! Please respond with 'Connection successful'")
            if "successful" in response.text.lower():
                self.console.print("[green]✅ Gemini API connection successful[/green]")
                return True
            else:
                self.console.print("[yellow]⚠️  Gemini API responded but with unexpected content[/yellow]")
                return False
                
        except Exception as e:
            self.console.print(f"[red]❌ Gemini API connection failed: {e}[/red]")
            return False
    
    def test_browserbase_configuration(self) -> bool:
        """Test Browserbase configuration (basic validation)."""
        api_key = os.getenv("BROWSERBASE_API_KEY")
        project_id = os.getenv("BROWSERBASE_PROJECT_ID")
        
        if not api_key or api_key == "your_browserbase_api_key_here":
            self.console.print("[red]❌ Browserbase API key not configured[/red]")
            return False
        
        if not project_id or project_id == "your_browserbase_project_id_here":
            self.console.print("[red]❌ Browserbase Project ID not configured[/red]")
            return False
        
        # Basic format validation
        if len(api_key) < 10:
            self.console.print("[yellow]⚠️  Browserbase API key seems too short[/yellow]")
            return False
        
        self.console.print("[green]✅ Browserbase configuration looks valid[/green]")
        return True
    
    def display_status(self) -> None:
        """Display the current configuration status."""
        self.console.print(Panel(
            "[bold cyan]MCP Surf Demo - Configuration Status[/bold cyan]",
            title="Configuration Check",
            border_style="cyan"
        ))
        
        table = Table(title="Configuration Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Notes", style="dim")
        
        status = self.check_configuration()
        
        # Environment file
        env_exists = self.env_file.exists()
        table.add_row(
            ".env file",
            "✅ Found" if env_exists else "❌ Missing",
            "Required for API keys" if not env_exists else ""
        )
        
        # Gemini API
        table.add_row(
            "Gemini API Key",
            "✅ Configured" if status["gemini"] else "❌ Missing",
            "Get from Google AI Studio" if not status["gemini"] else ""
        )
        
        # Browserbase API Key
        table.add_row(
            "Browserbase API Key",
            "✅ Configured" if status["browserbase_key"] else "❌ Missing",
            "Get from Browserbase dashboard" if not status["browserbase_key"] else ""
        )
        
        # Browserbase Project ID
        table.add_row(
            "Browserbase Project ID",
            "✅ Configured" if status["browserbase_project"] else "❌ Missing",
            "Get from Browserbase dashboard" if not status["browserbase_project"] else ""
        )
        
        self.console.print(table)
    
    def setup_wizard(self) -> None:
        """Run the setup wizard."""
        self.console.print(Panel(
            "[bold cyan]🧙‍♂️ MCP Surf Demo Setup Wizard[/bold cyan]\n\n"
            "This wizard will help you configure your environment for the MCP Surf Demo.\n"
            "You'll need:\n"
            "• Google Gemini API key\n"
            "• Browserbase API key and Project ID",
            title="Setup Wizard",
            border_style="cyan"
        ))
        
        # Check and create .env file
        self.check_env_file()
        
        # Guide user through configuration
        status = self.check_configuration()
        
        if not status["gemini"]:
            self.console.print("\n[yellow]📝 Gemini API Key Setup[/yellow]")
            self.console.print("1. Go to https://makersuite.google.com/app/apikey")
            self.console.print("2. Sign in with your Google account")
            self.console.print("3. Create a new API key")
            self.console.print("4. Copy the key and paste it in your .env file")
            
            if Confirm.ask("Have you updated your .env file with the Gemini API key?"):
                load_dotenv(override=True)  # Reload environment
        
        if not status["browserbase_key"] or not status["browserbase_project"]:
            self.console.print("\n[yellow]📝 Browserbase Setup[/yellow]")
            self.console.print("1. Go to https://www.browserbase.com/")
            self.console.print("2. Sign up for an account")
            self.console.print("3. Get your API key and Project ID from the dashboard")
            self.console.print("4. Update your .env file with both values")
            
            if Confirm.ask("Have you updated your .env file with Browserbase credentials?"):
                load_dotenv(override=True)  # Reload environment
        
        # Test connections
        if Confirm.ask("\nWould you like to test your API connections?"):
            self.test_connections()
        
        self.console.print("\n[green]🎉 Setup complete! You can now run the demo with:[/green]")
        self.console.print("[cyan]python main.py[/cyan]")
    
    def test_connections(self) -> None:
        """Test all API connections."""
        self.console.print("\n[yellow]🧪 Testing API Connections...[/yellow]")
        
        # Test Gemini
        self.console.print("\n1. Testing Gemini API...")
        gemini_ok = self.test_gemini_connection()
        
        # Test Browserbase (basic validation)
        self.console.print("\n2. Testing Browserbase configuration...")
        browserbase_ok = self.test_browserbase_configuration()
        
        if gemini_ok and browserbase_ok:
            self.console.print("\n[green]🎉 All tests passed! You're ready to go![/green]")
        else:
            self.console.print("\n[red]❌ Some tests failed. Please check your configuration.[/red]")


def main():
    """Main function."""
    helper = ConfigHelper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            helper.display_status()
        elif command == "test":
            helper.test_connections()
        elif command == "setup":
            helper.setup_wizard()
        else:
            print("Usage: python config.py [status|test|setup]")
    else:
        helper.setup_wizard()


if __name__ == "__main__":
    main()
