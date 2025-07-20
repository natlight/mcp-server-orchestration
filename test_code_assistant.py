#!/usr/bin/env python3
"""
Test script for the Code Assistant MCP Server

This script demonstrates how to use the code assistant server
to generate code with proper standards and documentation.
"""

import json
import subprocess
import sys
import time
import os

def test_code_assistant():
    """Test the code assistant server functionality"""
    
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required")
        print("Please set it with: export OPENAI_API_KEY=your_api_key")
        return False
    
    print("Testing Code Assistant MCP Server...")
    
    try:
        # Start the code assistant server
        print("Starting code assistant server...")
        process = subprocess.Popen([
            sys.executable, "code-assistant-server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        # Give the server time to start
        time.sleep(5)
        
        # Test 1: Check server status
        print("\nTest 1: Checking server status...")
        status_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_server_status",
                "arguments": {}
            }
        }
        
        process.stdin.write((json.dumps(status_request) + "\n").encode())
        process.stdin.flush()
        
        response_line = process.stdout.readline().decode().strip()
        if response_line:
            response = json.loads(response_line)
            print(f"Server status: {response}")
        
        # Test 2: Get available languages
        print("\nTest 2: Getting available languages...")
        languages_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_available_languages",
                "arguments": {}
            }
        }
        
        process.stdin.write((json.dumps(languages_request) + "\n").encode())
        process.stdin.flush()
        
        response_line = process.stdout.readline().decode().strip()
        if response_line:
            response = json.loads(response_line)
            print(f"Available languages: {response}")
        
        # Test 3: Generate simple Python code
        print("\nTest 3: Generating Python code...")
        code_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "generate_code_with_context",
                "arguments": {
                    "request": "Create a simple function to calculate the factorial of a number",
                    "language": "python",
                    "include_tests": True,
                    "include_docs": True
                }
            }
        }
        
        process.stdin.write((json.dumps(code_request) + "\n").encode())
        process.stdin.flush()
        
        response_line = process.stdout.readline().decode().strip()
        if response_line:
            response = json.loads(response_line)
            print(f"Generated code: {response}")
        
        print("\nTests completed successfully!")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()

def test_simple_import():
    """Test if we can import the required modules"""
    print("Testing module imports...")
    
    try:
        import fastmcp
        print("✓ fastmcp imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import fastmcp: {e}")
        return False
    
    try:
        import agents
        print("✓ openai-agents imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import openai-agents: {e}")
        print("Install with: pip install openai-agents")
        return False
    
    try:
        import pydantic
        print("✓ pydantic imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pydantic: {e}")
        return False
    
    print("All modules imported successfully!")
    return True

if __name__ == "__main__":
    print("Code Assistant MCP Server Test Suite")
    print("=" * 40)
    
    # Test imports first
    if not test_simple_import():
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    
    # Test the server functionality
    if test_code_assistant():
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)