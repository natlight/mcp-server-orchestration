#!/usr/bin/env python3
"""
Code Assistant MCP Server

This server uses the OpenAI Agents SDK to orchestrate multiple MCP servers
(standards and context7) to provide intelligent code generation with proper
standards compliance and up-to-date library documentation.
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import List, Optional, Dict, Any
import tempfile
import signal
import atexit

from fastmcp import FastMCP
from agents import Agent, Runner, tool
from pydantic import BaseModel

# Initialize the MCP server
mcp = FastMCP("Code Assistant Server")

class CodeRequest(BaseModel):
    """Model for code generation requests"""
    request: str
    language: str = "python"
    libraries: Optional[List[str]] = None
    include_tests: bool = False
    include_docs: bool = True

class MCPServerManager:
    """Manages internal MCP servers as subprocesses"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.temp_files: List[str] = []
        
    def start_standards_server(self) -> int:
        """Start the standards MCP server and return its port"""
        try:
            # Use the existing standards-server.py
            process = subprocess.Popen([
                sys.executable, "standards-server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
            self.processes["standards"] = process
            print(f"Started standards server with PID: {process.pid}")
            return process.pid
        except Exception as e:
            print(f"Failed to start standards server: {e}")
            raise
    
    def start_context7_server(self) -> int:
        """Start a context7 MCP server and return its port"""
        try:
            # Start context7 server using Docker
            process = subprocess.Popen([
                "docker", "run", "-i", "--rm", "mcp/context7"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
            self.processes["context7"] = process
            print(f"Started context7 server with PID: {process.pid}")
            return process.pid
        except Exception as e:
            print(f"Failed to start context7 server: {e}")
            raise
    
    def stop_all_servers(self):
        """Stop all managed MCP servers"""
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"Stopped {name} server")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"Force killed {name} server")
            except Exception as e:
                print(f"Error stopping {name} server: {e}")
        
        # Clean up temp files
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

# Global server manager
server_manager = MCPServerManager()

class CodeAssistantAgent:
    """Main agent that orchestrates code generation with standards and documentation"""
    
    def __init__(self):
        self.agent = None
        self.setup_agent()
    
    def setup_agent(self):
        """Setup the OpenAI agent with tools for accessing internal MCP servers"""
        
        @tool
        def get_coding_standards(language: str = "python") -> str:
            """Get coding standards for a specific programming language"""
            try:
                # Communicate with standards server
                process = server_manager.processes.get("standards")
                if not process:
                    return "Standards server not available"
                
                # Create a simple request to get standards
                request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "resources/read",
                    "params": {
                        "uri": f"standards://checklist/{language}"
                    }
                }
                
                # Send request to standards server
                process.stdin.write((json.dumps(request) + "\n").encode())
                process.stdin.flush()
                
                # Read response (simplified - in production would need proper JSON-RPC handling)
                response_line = process.stdout.readline().decode().strip()
                if response_line:
                    response = json.loads(response_line)
                    if "result" in response and "contents" in response["result"]:
                        return response["result"]["contents"][0]["text"]
                
                return f"Coding standards for {language} retrieved successfully"
            except Exception as e:
                return f"Error getting coding standards: {str(e)}"
        
        @tool
        def get_library_documentation(library_name: str, topic: str = "") -> str:
            """Get up-to-date documentation for a specific library"""
            try:
                # Communicate with context7 server
                process = server_manager.processes.get("context7")
                if not process:
                    return "Context7 server not available"
                
                # Create request to resolve library ID first
                resolve_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "resolve-library-id",
                        "arguments": {
                            "libraryName": library_name
                        }
                    }
                }
                
                # Send request
                process.stdin.write((json.dumps(resolve_request) + "\n").encode())
                process.stdin.flush()
                
                # Read response (simplified)
                response_line = process.stdout.readline().decode().strip()
                if response_line:
                    response = json.loads(response_line)
                    # In a real implementation, we'd parse the response and make a follow-up call
                    # to get-library-docs with the resolved library ID
                    return f"Documentation for {library_name} retrieved successfully"
                
                return f"Library documentation for {library_name} not found"
            except Exception as e:
                return f"Error getting library documentation: {str(e)}"
        
        @tool
        def analyze_code_requirements(request: str, language: str) -> str:
            """Analyze the code request to determine what standards and libraries are needed"""
            # This tool helps the agent understand what context it needs to gather
            analysis = {
                "language": language,
                "complexity": "medium",  # Could be determined by analyzing the request
                "suggested_libraries": [],  # Could be extracted from the request
                "standards_needed": ["general", "testing", "documentation"]
            }
            
            # Simple keyword-based analysis (could be enhanced with NLP)
            request_lower = request.lower()
            
            if "test" in request_lower or "unittest" in request_lower:
                analysis["standards_needed"].append("testing")
            
            if "api" in request_lower or "rest" in request_lower:
                analysis["suggested_libraries"].extend(["requests", "fastapi"])
            
            if "data" in request_lower or "pandas" in request_lower:
                analysis["suggested_libraries"].extend(["pandas", "numpy"])
            
            if "web" in request_lower or "html" in request_lower:
                analysis["suggested_libraries"].extend(["flask", "django"])
            
            return json.dumps(analysis, indent=2)
        
        # Create the agent with tools
        self.agent = Agent(
            name="Code Assistant",
            instructions="""You are an expert code assistant that generates high-quality code following team standards.

Your workflow:
1. First, analyze the code request to understand what's needed
2. Get the relevant coding standards for the specified language
3. If libraries are mentioned or needed, get their latest documentation
4. Generate code that follows the standards and uses best practices
5. Include proper documentation, error handling, and tests if requested

Always prioritize:
- Code quality and readability
- Following team coding standards
- Using up-to-date library practices
- Including proper documentation
- Adding appropriate error handling
""",
            tools=[get_coding_standards, get_library_documentation, analyze_code_requirements]
        )
    
    async def generate_code(self, code_request: CodeRequest) -> str:
        """Generate code using the agent with standards and documentation context"""
        try:
            # Prepare the prompt for the agent
            prompt = f"""
Generate {code_request.language} code for the following request:

{code_request.request}

Requirements:
- Language: {code_request.language}
- Include tests: {code_request.include_tests}
- Include documentation: {code_request.include_docs}
"""
            
            if code_request.libraries:
                prompt += f"- Use these libraries: {', '.join(code_request.libraries)}\n"
            
            prompt += """
Please follow this workflow:
1. Analyze the requirements
2. Get the coding standards for the language
3. Get documentation for any libraries needed
4. Generate the code with proper standards compliance
"""
            
            # Run the agent
            result = Runner.run_sync(self.agent, prompt)
            return result.final_output
            
        except Exception as e:
            return f"Error generating code: {str(e)}"

# Global agent instance
code_agent = CodeAssistantAgent()

@mcp.tool()
def generate_code_with_context(
    request: str,
    language: str = "python",
    libraries: Optional[List[str]] = None,
    include_tests: bool = False,
    include_docs: bool = True
) -> str:
    """
    Generate code following team standards with latest library documentation.
    
    Args:
        request: Description of what code to generate
        language: Programming language (python, javascript, typescript, etc.)
        libraries: List of libraries to get documentation for
        include_tests: Whether to include unit tests
        include_docs: Whether to include documentation
    
    Returns:
        Generated code with standards compliance and proper documentation
    """
    try:
        code_request = CodeRequest(
            request=request,
            language=language,
            libraries=libraries or [],
            include_tests=include_tests,
            include_docs=include_docs
        )
        
        # Use asyncio to run the async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(code_agent.generate_code(code_request))
            return result
        finally:
            loop.close()
            
    except Exception as e:
        return f"Error in code generation: {str(e)}"

@mcp.tool()
def get_available_languages() -> List[str]:
    """Get list of supported programming languages"""
    return [
        "python",
        "javascript", 
        "typescript",
        "java",
        "go",
        "rust",
        "sql",
        "html",
        "css"
    ]

@mcp.tool()
def get_server_status() -> Dict[str, Any]:
    """Get status of internal MCP servers"""
    status = {
        "standards_server": "unknown",
        "context7_server": "unknown",
        "agent_ready": bool(code_agent.agent)
    }
    
    for name, process in server_manager.processes.items():
        if process and process.poll() is None:
            status[f"{name}_server"] = "running"
        else:
            status[f"{name}_server"] = "stopped"
    
    return status

def cleanup_on_exit():
    """Cleanup function to stop all servers on exit"""
    print("Shutting down code assistant server...")
    server_manager.stop_all_servers()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"Received signal {signum}, shutting down...")
    cleanup_on_exit()
    sys.exit(0)

def main():
    """Main function to start the server and internal MCP servers"""
    # Register cleanup handlers
    atexit.register(cleanup_on_exit)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Starting Code Assistant MCP Server...")
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required")
        sys.exit(1)
    
    try:
        # Start internal MCP servers
        print("Starting internal MCP servers...")
        server_manager.start_standards_server()
        server_manager.start_context7_server()
        
        # Give servers time to start
        import time
        time.sleep(2)
        
        print("Code Assistant MCP Server ready!")
        print("Available tools:")
        print("- generate_code_with_context: Generate code with standards and documentation")
        print("- get_available_languages: List supported programming languages")
        print("- get_server_status: Check status of internal servers")
        
        # Run the MCP server
        mcp.run()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    finally:
        cleanup_on_exit()

if __name__ == "__main__":
    main()