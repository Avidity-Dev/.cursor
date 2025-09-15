# How to Build an MCP Server: A Comprehensive Guide

This guide is based on analysis of multiple MCP server implementations (dbt-mcp, linear-cline, obsidian) and provides a flexible approach to building production-ready MCP (Model Context Protocol) servers in both Python and TypeScript.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Choosing Your Stack](#choosing-your-stack)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [Implementation Steps](#implementation-steps)
6. [Testing Strategy](#testing-strategy)
7. [Best Practices](#best-practices)

## Architecture Overview

MCP servers can follow different architectural patterns depending on your needs:

### Pattern 1: FastMCP with Tool Decorators (Python)
Used by dbt-mcp, this pattern uses FastMCP's decorator-based approach:

```
┌─────────────────┐
│   Entry Point   │ → main.py
└────────┬────────┘
         │
┌────────▼────────┐
│  FastMCP Server │ → Subclass with lifecycle hooks
└────────┬────────┘
         │
┌────────▼────────┐
│ Tool Registry   │ → Functions with @mcp.tool decorator
└────────┬────────┘
         │
┌────────▼────────┐
│ External APIs   │ → Client implementations
└─────────────────┘
```

### Pattern 2: Handler-Based Architecture (TypeScript/Python)
Used by linear-cline (TypeScript) and obsidian (Python), this pattern uses handler classes:

```
┌─────────────────┐
│   Entry Point   │ → index.ts/server.py
└────────┬────────┘
         │
┌────────▼────────┐
│   MCP Server    │ → SDK Server instance
└────────┬────────┘
         │
┌────────▼────────┐
│ Handler Factory │ → Routes tools to handlers
└────────┬────────┘
         │
┌────────▼────────┐
│  Tool Handlers  │ → Classes implementing tool logic
└────────┬────────┘
         │
┌────────▼────────┐
│ External APIs   │ → Client implementations
└─────────────────┘
```

## Choosing Your Stack

### Language Choice

**Python** - Choose when:
- You need data science libraries (pandas, numpy)
- Integration with ML/AI frameworks
- Rapid prototyping
- Your team is Python-focused

**TypeScript** - Choose when:
- You need strong typing throughout
- Building complex domain models
- Integration with Node.js ecosystem
- Your team prefers TypeScript

### Architecture Pattern Choice

**FastMCP Pattern** - Choose when:
- Building simple to medium complexity servers
- Want minimal boilerplate
- Prefer functional programming style
- Need quick implementation

**Handler Pattern** - Choose when:
- Building complex servers with many tools
- Need clear separation of concerns
- Want to group related tools together
- Prefer object-oriented design

## Project Structure

### Python FastMCP Structure (dbt-mcp style)
```
your-mcp-server/
├── pyproject.toml          # Project configuration
├── src/
│   ├── your_mcp/
│   │   ├── __init__.py
│   │   ├── main.py         # Entry point
│   │   ├── mcp/
│   │   │   └── server.py   # FastMCP server implementation
│   │   ├── config/
│   │   │   └── config.py   # Configuration management
│   │   ├── tools/          # Tool implementations
│   │   │   ├── feature1/
│   │   │   │   └── tools.py
│   │   │   └── feature2/
│   │   │       └── tools.py
│   │   ├── clients/        # External API clients
│   │   │   └── api_client.py
│   │   └── prompts/        # Tool descriptions
│   │       ├── prompts.py
│   │       └── feature1/
│   │           └── tool1.md
├── tests/
│   ├── unit/
│   └── integration/
└── .env.example
```

### Python Handler Structure (obsidian style)
```
your-mcp-server/
├── pyproject.toml
├── src/
│   ├── mcp_yourservice/
│   │   ├── __init__.py
│   │   ├── server.py       # Server setup and tool registry
│   │   ├── tools.py        # Tool handler classes
│   │   └── yourservice.py  # API client
└── README.md
```

### TypeScript Handler Structure (linear-cline style)
```
your-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts            # Entry point
│   ├── core/
│   │   ├── handlers/
│   │   │   ├── base.handler.ts
│   │   │   └── handler.factory.ts
│   │   ├── interfaces/
│   │   │   └── tool-handler.interface.ts
│   │   └── types/
│   │       └── tool.types.ts
│   ├── features/
│   │   ├── feature1/
│   │   │   ├── handlers/
│   │   │   │   └── feature1.handler.ts
│   │   │   └── types/
│   │   │       └── feature1.types.ts
│   │   └── feature2/
│   │       ├── handlers/
│   │       └── types/
│   └── external/
│       └── client.ts
└── tests/

## Core Components

### 1. Entry Points

#### Python FastMCP Entry Point
```python
# src/your_mcp/main.py
import asyncio
from your_mcp.mcp.server import create_your_mcp

def main() -> None:
    asyncio.run(create_your_mcp()).run()

main()
```

#### Python Handler Entry Point
```python
# src/mcp_yourservice/server.py (main entry)
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from . import tools

load_dotenv()

app = Server("mcp-yourservice")

# Register tool handlers
tool_handlers = {}
tool_handlers["tool1"] = tools.Tool1Handler()
tool_handlers["tool2"] = tools.Tool2Handler()

@app.list_tools()
async def list_tools():
    return [handler.get_tool_description() for handler in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name not in tool_handlers:
        raise ValueError(f"Unknown tool: {name}")
    return tool_handlers[name].run_tool(arguments)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
```

#### TypeScript Entry Point
```typescript
// src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { HandlerFactory } from './core/handlers/handler.factory.js';

class YourServer {
  private server: Server;
  private handlerFactory: HandlerFactory;

  constructor() {
    this.server = new Server(
      { name: 'your-server', version: '1.0.0' },
      { capabilities: { tools: {} } }
    );
    
    this.handlerFactory = new HandlerFactory();
    this.setupRequestHandlers();
  }

  private setupRequestHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: this.handlerFactory.getAvailableTools(),
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { handler, method } = this.handlerFactory.getHandlerForTool(request.params.name);
      return await handler[method](request.params.arguments);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

const server = new YourServer();
server.run().catch(console.error);
```

### 2. Server Implementations

#### Python FastMCP Server

```python
# src/your_mcp/mcp/server.py
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Any, Sequence

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent, EmbeddedResource

from your_mcp.config.config import load_config
from your_mcp.tools.tool1 import register_tool1_tools
from your_mcp.tools.tool2 import register_tool2_tools

logger = logging.getLogger(__name__)
config = load_config()

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[None]:
    logger.info("Starting MCP server")
    try:
        yield
    except Exception as e:
        logger.error(f"Error in MCP server: {e}")
        raise e
    finally:
        logger.info("Shutting down MCP server")

class YourMCP(FastMCP):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
    async def call_tool(
        self, name: str, arguments: dict[str, Any]
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        logger.info(f"Calling tool: {name}")
        try:
            result = await super().call_tool(name, arguments)
            logger.info(f"Tool {name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=str(e))]

async def create_your_mcp():
    mcp = YourMCP(name="your-mcp", lifespan=app_lifespan)
    
    # Register tools based on configuration
    if config.feature1_enabled:
        register_tool1_tools(mcp, config.feature1_config)
    
    if config.feature2_enabled:
        register_tool2_tools(mcp, config.feature2_config)
    
    return mcp
```

### 3. Configuration Management

```python
# src/your_mcp/config/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Feature1Config:
    api_key: str
    base_url: str

@dataclass
class Config:
    feature1_enabled: bool
    feature1_config: Feature1Config | None
    feature2_enabled: bool

def load_config() -> Config:
    load_dotenv()
    
    # Read environment variables
    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("BASE_URL", "https://api.example.com")
    disable_feature1 = os.environ.get("DISABLE_FEATURE1", "false") == "true"
    
    # Validate required configuration
    errors = []
    if not disable_feature1 and not api_key:
        errors.append("API_KEY is required when Feature1 is enabled")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(errors))
    
    # Build configuration
    feature1_config = None
    if not disable_feature1 and api_key:
        feature1_config = Feature1Config(
            api_key=api_key,
            base_url=base_url
        )
    
    return Config(
        feature1_enabled=not disable_feature1,
        feature1_config=feature1_config,
        feature2_enabled=True  # Example of always-enabled feature
    )
```

### 4. Tool Implementation Patterns

#### Python FastMCP Tools (Decorator Pattern)
```python
# src/your_mcp/tools/feature1/tools.py
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from your_mcp.config.config import Feature1Config
from your_mcp.clients.api_client import APIClient
from your_mcp.prompts.prompts import get_prompt

def register_feature1_tools(mcp: FastMCP, config: Feature1Config) -> None:
    client = APIClient(config.api_key, config.base_url)
    
    @mcp.tool(description=get_prompt("feature1/list_items"))
    def list_items(
        filter: str | None = Field(default=None, description="Optional filter")
    ) -> list[dict] | str:
        try:
            return client.get_items(filter=filter)
        except Exception as e:
            return f"Error: {str(e)}"
```

#### Python Handler Pattern
```python
# src/mcp_yourservice/tools.py
from mcp.types import Tool, TextContent
import json

class ToolHandler:
    def __init__(self, tool_name: str):
        self.name = tool_name

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()

    def run_tool(self, args: dict) -> list[TextContent]:
        raise NotImplementedError()

class ListItemsHandler(ToolHandler):
    def __init__(self, api_client):
        super().__init__("list_items")
        self.api_client = api_client

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="List all items",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "Filter items"}
                }
            }
        )

    def run_tool(self, args: dict):
        items = self.api_client.list_items(args.get("filter"))
        return [TextContent(type="text", text=json.dumps(items, indent=2))]
```

#### TypeScript Handler Pattern
```typescript
// src/features/items/handlers/item.handler.ts
import { BaseHandler } from '../../../core/handlers/base.handler.js';
import { BaseToolResponse } from '../../../core/interfaces/tool-handler.interface.js';

export class ItemHandler extends BaseHandler {
  async handleListItems(args: { filter?: string }): Promise<BaseToolResponse> {
    try {
      const client = this.verifyAuth();
      const items = await client.getItems(args.filter);
      return this.createJsonResponse(items);
    } catch (error) {
      this.handleError(error, 'list items');
    }
  }

  async handleGetItem(args: { itemId: string }): Promise<BaseToolResponse> {
    this.validateRequiredParams(args, ['itemId']);
    try {
      const client = this.verifyAuth();
      const item = await client.getItem(args.itemId);
      return this.createJsonResponse(item);
    } catch (error) {
      this.handleError(error, 'get item');
    }
  }
}
```

### 5. Prompt Management

```python
# src/your_mcp/prompts/prompts.py
from pathlib import Path

def get_prompt(name: str) -> str:
    """Load prompt from markdown file."""
    return (Path(__file__).parent / f"{name}.md").read_text()
```

Create descriptive markdown files for each tool:

```markdown
# src/your_mcp/prompts/tool1/list_items.md
List items from the external service. 
Returns a list of items with their basic properties.
Use the filter parameter to narrow results.
```

### 6. External API Client

```python
# src/your_mcp/clients/api_client.py
import requests
from typing import Any

class APIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def get_items(self, filter: str | None = None) -> list[dict]:
        params = {"filter": filter} if filter else {}
        response = self.session.get(
            f"{self.base_url}/items",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_item(self, item_id: str) -> dict:
        response = self.session.get(
            f"{self.base_url}/items/{item_id}"
        )
        response.raise_for_status()
        return response.json()
```

## Implementation Steps

### Step 1: Set Up Your Project

#### Python Setup

```bash
# Create project structure
mkdir your-mcp-server
cd your-mcp-server

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "your-mcp-server"
description = "MCP server for YourService"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.1.0",           # For handler pattern
    # OR
    "mcp[cli]>=1.6.0",      # For FastMCP pattern
    "python-dotenv>=1.0.0",
    "requests>=2.32.0",
]

[project.scripts]
your-mcp = "your_mcp.main:main"  # FastMCP
# OR
mcp-yourservice = "mcp_yourservice:main"  # Handler pattern

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF
```

#### TypeScript Setup

```bash
# Create project
mkdir your-mcp-server
cd your-mcp-server

# Initialize package.json
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk @linear/sdk graphql
npm install -D typescript @types/node jest ts-jest nodemon

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
EOF

# Update package.json scripts
npm pkg set scripts.build="tsc"
npm pkg set scripts.start="node build/index.js"
npm pkg set scripts.dev="nodemon --watch src --ext ts --exec 'npm run build && npm start'"
npm pkg set type="module"
```

### Step 2: Create Basic Structure

```bash
# Create directory structure
mkdir -p src/your_mcp/{mcp,config,tools,clients,prompts}
touch src/your_mcp/__init__.py
touch src/your_mcp/main.py
```

### Step 3: Implement Core Server

Follow the code examples above to implement:
1. main.py entry point
2. MCP server class
3. Configuration loader
4. First tool implementation

### Step 4: Test Your Server

#### Python Testing
```bash
# Install dependencies
pip install -e .  # or: uv sync

# Test with MCP Inspector
npx @modelcontextprotocol/inspector your-mcp

# Or run directly
python -m your_mcp.main
```

#### TypeScript Testing
```bash
# Build the project
npm run build

# Test with MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js

# Or use dev mode
npm run dev
```

### Step 5: Add to MCP Client

#### Claude Desktop Configuration

For Python servers:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "your-mcp",  // or "mcp-yourservice"
      "env": {
        "API_KEY": "your-api-key",
        "OTHER_VAR": "value"
      }
    }
  }
}
```

For TypeScript servers:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["/path/to/your-server/build/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

## Testing Strategy

### Unit Tests

```python
# tests/unit/tools/test_tool1.py
import pytest
from unittest.mock import Mock
from your_mcp.tools.tool1 import register_tool1_tools

@pytest.fixture
def mock_mcp():
    class MockMCP:
        def __init__(self):
            self.tools = {}
        
        def tool(self, **kwargs):
            def decorator(func):
                self.tools[func.__name__] = func
                return func
            return decorator
    
    return MockMCP()

def test_list_items(mock_mcp, monkeypatch):
    # Mock the API client
    mock_client = Mock()
    mock_client.get_items.return_value = [{"id": "1", "name": "Item 1"}]
    
    # Register tools
    config = Mock(api_key="test", base_url="http://test")
    register_tool1_tools(mock_mcp, config)
    
    # Test the tool
    result = mock_mcp.tools["list_items"](filter="test")
    assert len(result) == 1
    assert result[0]["name"] == "Item 1"
```

### Integration Tests

```python
# tests/integration/test_server.py
import pytest
import asyncio
from your_mcp.mcp.server import create_your_mcp

@pytest.mark.asyncio
async def test_server_creation():
    server = await create_your_mcp()
    assert server.name == "your-mcp"
    
    # Test tool registration
    tools = server.get_tools()
    assert len(tools) > 0
```

## Best Practices

### 1. Error Handling

**Consistent Error Responses**
- Always return structured error messages
- Include context about what failed
- Log errors with appropriate levels

```python
# Good - Provides context
try:
    result = api.get_item(item_id)
except APIError as e:
    return f"Failed to fetch item {item_id}: {e.message}"
except Exception as e:
    logger.error(f"Unexpected error fetching item {item_id}: {e}")
    return f"An unexpected error occurred"

# TypeScript example
protected handleError(error: unknown, operation: string): never {
  throw new McpError(
    ErrorCode.InternalError,
    `Failed to ${operation}: ${error instanceof Error ? error.message : 'Unknown error'}`
  );
}
```

### 2. Configuration Management

**Environment Variables**
- Use `.env` files for local development
- Never commit secrets
- Validate all required config on startup
- Group related configuration

```python
# Group related config
@dataclass
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str

# Validate on load
def load_config():
    errors = []
    if not os.getenv("API_KEY"):
        errors.append("API_KEY is required")
    if errors:
        raise ValueError("\n".join(errors))
```

### 3. Tool Design Principles

**Single Responsibility**
- Each tool should do one thing well
- Avoid combining unrelated operations
- Make tool names action-oriented

```python
# Good - Clear, single purpose
@mcp.tool(description="Create a new issue in the project")
def create_issue(title: str, description: str, project_id: str): ...

# Bad - Does too much
@mcp.tool(description="Create issue and assign to user and add tags")
def create_and_setup_issue(...): ...
```

**Input Validation**
- Use Pydantic models or TypeScript interfaces
- Provide clear parameter descriptions
- Set sensible defaults

```python
# Python with Pydantic
def search_items(
    query: str = Field(description="Search query", min_length=1),
    limit: int = Field(default=10, ge=1, le=100, description="Max results"),
    include_archived: bool = Field(default=False, description="Include archived items")
): ...

# TypeScript with validation
protected validateRequiredParams<T>(params: T, required: Array<keyof T>): void {
  const missing = required.filter(param => !params[param]);
  if (missing.length > 0) {
    throw new McpError(ErrorCode.InvalidParams, `Missing: ${missing.join(', ')}`);
  }
}
```

### 4. Architecture Patterns

**Choose Based on Complexity**

| Pattern | Use When | Example |
|---------|----------|---------|
| FastMCP | 5-15 simple tools | File operations, simple API calls |
| Handler Classes | 15+ tools or complex domains | Multi-resource APIs, complex workflows |
| Feature Modules | Multiple related tool groups | Separate auth, CRUD, admin tools |

### 5. Testing Strategies

**Test at Multiple Levels**
- Unit tests for individual functions
- Integration tests for API interactions
- End-to-end tests for full tool execution

```python
# Mock external dependencies
@pytest.fixture
def mock_api_client():
    client = Mock()
    client.get_items.return_value = [{"id": "1", "name": "Test"}]
    return client

# Test error handling
def test_handles_api_error(mock_mcp, mock_api_client):
    mock_api_client.get_items.side_effect = APIError("Connection failed")
    result = mock_mcp.tools["list_items"]()
    assert "Failed" in result
```

### 6. Performance Optimization

**Efficient API Usage**
- Batch operations when possible
- Implement caching for read-heavy operations
- Use connection pooling

```python
# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_details(user_id: str):
    return api.get_user(user_id)

# Connection pooling
class APIClient:
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
        self.session.mount('https://', adapter)
```

### 7. Documentation Standards

**Tool Descriptions**
- Start with an action verb
- Explain what the tool does, not how
- Include important limitations

```markdown
# Good tool descriptions
"Search for issues matching specified criteria"
"Create a new project with optional template"
"Delete a file after confirmation"

# Include examples in prompt files
Search for issues using various filters:
- By status: status:open
- By assignee: assignee:john
- By date: created:>2024-01-01
```

### 8. Security Best Practices

**API Key Management**
- Rotate keys regularly
- Use least-privilege principles
- Implement key refresh for long-running servers

```python
# Auto-refresh pattern
class AuthManager:
    def __init__(self):
        self.token_expires_at = None
    
    def get_token(self):
        if self.needs_refresh():
            self.refresh_token()
        return self.current_token
```

### 9. Observability

**Structured Logging**
```python
import structlog
logger = structlog.get_logger()

logger.info("tool_called", 
    tool_name=name, 
    duration_ms=elapsed,
    user_id=user_id,
    success=True
)
```

**Metrics Collection**
```python
class UsageTracker:
    def track_tool_call(self, tool_name: str, duration: float, success: bool):
        # Send to metrics service
        metrics.increment(f"mcp.tool.{tool_name}.calls")
        metrics.histogram(f"mcp.tool.{tool_name}.duration", duration)
```

## Advanced Features

### Custom Tool Decorators

```python
def with_retry(max_attempts=3):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
        return wrapper
    return decorator

@mcp.tool(description="Fetch data with retry")
@with_retry(max_attempts=3)
async def fetch_data():
    # Implementation
    pass
```

### Streaming Responses

```python
from mcp.types import TextContent

@mcp.tool(description="Stream large dataset")
async def stream_data():
    async def generate():
        for chunk in large_dataset:
            yield TextContent(type="text", text=process_chunk(chunk))
    
    return generate()
```

### Resource Management

```python
@mcp.resource(description="Configuration file")
async def get_config():
    return {
        "uri": "config://settings",
        "content": load_settings(),
        "mimeType": "application/json"
    }
```

## Real-World Examples

### Example 1: dbt-mcp (Python FastMCP)
- **Pattern**: FastMCP with decorators
- **Tools**: 20+ tools across 4 categories
- **Features**: Multi-environment support, GraphQL integration, usage tracking
- **Best for**: Complex enterprise integrations

### Example 2: linear-cline (TypeScript Handlers)
- **Pattern**: Domain-driven handler architecture
- **Tools**: Issue tracking, project management
- **Features**: OAuth support, GraphQL mutations, bulk operations
- **Best for**: SaaS integrations with complex domain models

### Example 3: obsidian (Python Handlers)
- **Pattern**: Simple handler classes
- **Tools**: File operations, search, content manipulation
- **Features**: REST API integration, batch operations
- **Best for**: Simpler integrations with clear tool boundaries

## Decision Matrix

| Criteria | FastMCP | Handler Pattern |
|----------|---------|-----------------|
| **Setup Speed** | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐ Moderate |
| **Scalability** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Type Safety** | ⭐⭐⭐ Good (Pydantic) | ⭐⭐⭐⭐⭐ Excellent (TS) |
| **Testing** | ⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐⭐ Very Easy |
| **Modularity** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Learning Curve** | ⭐⭐⭐⭐⭐ Minimal | ⭐⭐⭐ Moderate |

## Conclusion

Building an MCP server involves key decisions about:

1. **Language**: Python for rapid development, TypeScript for type safety
2. **Architecture**: FastMCP for simplicity, Handlers for scalability
3. **Structure**: Flat for small projects, modular for large ones
4. **Testing**: Always include unit and integration tests
5. **Documentation**: Clear tool descriptions and examples
6. **Security**: Proper secret management and input validation

Choose the approach that best fits your:
- Team's expertise
- Project complexity
- Integration requirements
- Performance needs
- Maintenance expectations

All patterns are production-ready when implemented with proper error handling, testing, and documentation.