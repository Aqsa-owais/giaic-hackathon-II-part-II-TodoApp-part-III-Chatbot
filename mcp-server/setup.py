#!/usr/bin/env python3
"""Setup script for MCP Server development environment."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return None


def setup_environment():
    """Set up the development environment."""
    print("Setting up MCP Server development environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✓ Created .env file from .env.example")
        print("  Please update .env with your actual database configuration")
    
    # Install dependencies
    print("Installing dependencies...")
    if run_command("pip install -r requirements.txt"):
        print("✓ Dependencies installed")
    else:
        print("✗ Failed to install dependencies")
        return False
    
    # Run basic tests
    print("Running basic tests...")
    if run_command("python -m pytest tests/test_setup.py -v"):
        print("✓ Basic tests passed")
    else:
        print("✗ Basic tests failed")
        return False
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update .env with your database URL")
    print("2. Run 'make validate' to check configuration")
    print("3. Run 'make test' to run all tests")
    print("4. Run 'make run' to start the MCP server")
    
    return True


if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)