"""Main MCP Server implementation."""

import asyncio
import logging
from typing import Any, Dict, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, TextContent

from .config import settings, validate_settings
from .database.layer import DatabaseLayer, DatabaseError


class TaskMCPServer:
    """MCP Server for task management tools.
    
    This server provides stateless task management capabilities through MCP tools.
    It exposes five core tools: add_task, list_tasks, update_task, complete_task, delete_task.
    All operations enforce strict user isolation and maintain no in-memory state.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize the MCP server with proper configuration.
        
        Args:
            database_url: Optional database URL override for testing
        """
        # Initialize FastMCP server with metadata
        self.mcp = FastMCP(settings.mcp_server_name)
        
        # Set up database layer integration
        self.db_layer = DatabaseLayer(database_url)
        
        # Configure server capabilities and register tools
        self._configure_server()
        self._register_tools()
    
    def _configure_server(self):
        """Configure server metadata and capabilities."""
        # Set server description and capabilities
        self.mcp.server_info = {
            "name": settings.mcp_server_name,
            "version": settings.mcp_server_version,
            "description": "Stateless MCP server for todo task management operations",
            "capabilities": {
                "tools": {
                    "listChanged": False  # Tools don't change dynamically
                }
            }
        }
        
        logging.info(f"Configured MCP server: {settings.mcp_server_name} v{settings.mcp_server_version}")
    
    def _register_tools(self):
        """Register all task management tools.
        
        This method will register the five core tools:
        - add_task: Create new tasks
        - list_tasks: Retrieve user tasks with optional filtering
        - update_task: Modify existing tasks
        - complete_task: Mark tasks as completed
        - delete_task: Remove tasks permanently
        
        Tools will be implemented in subsequent tasks.
        """
        # Tool registration will be implemented in task 3.2
        # Each tool will be registered with proper parameter validation
        # and consistent response formatting
        logging.info("Tool registration framework ready (tools to be implemented)")
        pass
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information for debugging and monitoring.
        
        Returns:
            Dictionary containing server metadata and status
        """
        return {
            "name": settings.mcp_server_name,
            "version": settings.mcp_server_version,
            "description": "Stateless MCP server for todo task management operations",
            "database_healthy": self.db_layer.health_check(),
            "tools_registered": 0,  # Will be updated as tools are implemented
            "capabilities": {
                "stateless_operation": True,
                "user_isolation": True,
                "postgresql_backend": True,
                "tools": ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
            }
        }
    
    async def run(self):
        """Run the MCP server with proper initialization and error handling."""
        try:
            # Validate configuration
            validate_settings()
            logging.info("Configuration validated successfully")
            
            # Check database connection
            if not self.db_layer.health_check():
                raise RuntimeError("Database connection failed - check DATABASE_URL")
            
            logging.info("Database connection established and healthy")
            logging.info(f"Starting {settings.mcp_server_name} v{settings.mcp_server_version}")
            logging.info("Server capabilities: Task management tools with user isolation")
            
            # Run the MCP server
            await self.mcp.run()
            
        except Exception as e:
            logging.error(f"Server startup failed: {e}")
            raise


def setup_logging():
    """Configure logging for the server."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


async def main():
    """Main entry point for the MCP server."""
    setup_logging()
    
    server = TaskMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())