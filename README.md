# MCP Server Orchestration

Demonstration of MCP server orchestration - an intelligent code assistant that manages and coordinates multiple MCP servers using OpenAI Agents SDK.

## Overview

**Question: Can an MCP server start up and orchestrate other MCP servers?**

**Answer: YES!** This repository demonstrates a sophisticated MCP server (`code-assistant-server.py`) that orchestrates multiple other MCP servers as internal components to provide intelligent code generation with proper standards compliance and up-to-date library documentation.

## Architecture

```
External MCP Client
        ↓
┌─────────────────────────────────────────┐
│        code-assistant-server.py         │ ← Main MCP Server
│                                         │
│  ┌─────────────────────────────────────┐ │
│  │        OpenAI Agent                 │ │ ← Orchestration Layer
│  │                                     │ │
│  │  ┌─────────────┐ ┌─────────────────┐│ │
│  │  │ Standards   │ │ Context7        ││ │ ← Internal MCP Clients
│  │  │ MCP Client  │ │ MCP Client      ││ │
│  │  └─────────────┘ └─────────────────┘│ │
│  └─────────────────────────────────────┘ │
│                                         │
│  ┌─────────────────────────────────────┐ │
│  │           MCP Server                │ │ ← External Interface
│  │      (External Interface)           │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
        ↓                    ↓
┌─────────────────┐  ┌─────────────────┐
│ standards-server│  │ context7 server │ ← Internal MCP Servers
│   (subprocess)  │  │   (subprocess)  │   (managed as subprocesses)
└─────────────────┘  └─────────────────┘
```

## Servers

### 1. Code Assistant MCP Server (`code-assistant-server.py`)

The main orchestrating server that:
- **Starts and manages other MCP servers as subprocesses**
- **Uses OpenAI Agents SDK** for intelligent orchestration
- **Communicates with internal MCP servers** via JSON-RPC
- **Provides intelligent code generation** with context from multiple sources

### 2. Team Coding Standards MCP Server (`standards-server.py`)

Provides access to team coding standards and best practices as resources.

## Key Features

- **MCP Server Orchestration**: Demonstrates that MCP servers can start and manage other MCP servers
- **Intelligent Agent Integration**: Uses OpenAI Agents SDK for smart coordination
- **Multi-Server Communication**: Combines coding standards and library documentation
- **Production-Ready**: Proper error handling, cleanup, and monitoring
- **Multiple Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust, SQL, HTML, CSS

## Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set OpenAI API Key:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

3. **Ensure Docker is running** (for Context7 server)

4. **Run the Code Assistant Server:**
```bash
python code-assistant-server.py
```

## Usage Examples

### Basic Code Generation
```json
{
  "method": "tools/call",
  "params": {
    "name": "generate_code_with_context",
    "arguments": {
      "request": "Create a REST API endpoint for user authentication",
      "language": "python",
      "libraries": ["fastapi", "pydantic"],
      "include_tests": true,
      "include_docs": true
    }
  }
}
```

### Check Server Status
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_server_status",
    "arguments": {}
  }
}
```

## Testing

Run the test suite:
```bash
python test_code_assistant.py
```

## Files

- **`code-assistant-server.py`** - Main orchestrating MCP server
- **`standards-server.py`** - Team coding standards MCP server
- **`test_code_assistant.py`** - Comprehensive test suite
- **`requirements.txt`** - Python dependencies
- **`mcp-config-example.json`** - MCP client configuration example
- **`IMPLEMENTATION_SUMMARY.md`** - Detailed technical documentation

## How It Works

1. **Startup**: Code assistant server starts internal MCP servers as subprocesses
2. **Request Processing**: External requests trigger the OpenAI Agent
3. **Context Gathering**: Agent fetches coding standards and library documentation
4. **Code Generation**: Agent generates context-aware code following best practices
5. **Response**: Complete solution returned with tests and documentation

## Benefits

- **Modularity**: Each MCP server has specific responsibilities
- **Intelligence**: Agent makes decisions about context gathering
- **Scalability**: Easy to add more internal MCP servers
- **Reusability**: Components can be used independently

## License

MIT License - see LICENSE file for details.
