"""Unit tests for MCP server initialization."""

import pytest
import os
import logging
from unittest.mock import patch, MagicMock, Mock

from src.server import TaskMCPServer, setup_logging
from src.config import settings
from src.database.layer import DatabaseLayer


class TestServerInitialization:
    """Test cases for server initialization."""
    
    def test_server_initializes_with_default_config(self):
        """Test that server initializes correctly with default configuration."""
        # Set up test database URL
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None) as mock_db_init:
                with patch.object(DatabaseLayer, 'health_check', return_value=True):
                    server = TaskMCPServer()
                    
                    # Verify server was initialized correctly
                    assert server is not None
                    assert hasattr(server, 'mcp')
                    assert hasattr(server, 'db_layer')
                    
                    # Verify database layer was initialized with correct URL
                    mock_db_init.assert_called_once_with(None)
    
    def test_server_initializes_with_custom_database_url(self):
        """Test that server initializes with custom database URL override."""
        custom_db_url = "postgresql://test:test@localhost/testdb"
        
        with patch.object(DatabaseLayer, '__init__', return_value=None) as mock_db_init:
            with patch.object(DatabaseLayer, 'health_check', return_value=True):
                server = TaskMCPServer(database_url=custom_db_url)
                
                # Verify server was initialized correctly
                assert server is not None
                assert hasattr(server, 'mcp')
                assert hasattr(server, 'db_layer')
                
                # Verify database layer was initialized with custom URL
                mock_db_init.assert_called_once_with(custom_db_url)
    
    def test_server_configuration_is_set_correctly(self):
        """Test that server metadata and capabilities are configured properly."""
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None):
                with patch.object(DatabaseLayer, 'health_check', return_value=True):
                    server = TaskMCPServer()
                    
                    # Verify server info is configured
                    server_info = server.get_server_info()
                    
                    assert server_info['name'] == settings.mcp_server_name
                    assert server_info['version'] == settings.mcp_server_version
                    assert server_info['description'] == "Stateless MCP server for todo task management operations"
                    assert 'capabilities' in server_info
                    assert server_info['capabilities']['stateless_operation'] is True
                    assert server_info['capabilities']['user_isolation'] is True
                    assert server_info['capabilities']['postgresql_backend'] is True
                    
                    # Verify expected tools are listed
                    expected_tools = ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
                    assert server_info['capabilities']['tools'] == expected_tools
    
    def test_database_connection_establishment(self):
        """Test that database connection is properly established during initialization."""
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None):
                with patch.object(DatabaseLayer, 'health_check', return_value=True) as mock_health_check:
                    server = TaskMCPServer()
                    
                    # Verify server info includes database health status
                    server_info = server.get_server_info()
                    assert server_info['database_healthy'] is True
                    
                    # Verify health check was called
                    mock_health_check.assert_called()
    
    def test_database_connection_failure_handling(self):
        """Test that server handles database connection failures gracefully."""
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None):
                with patch.object(DatabaseLayer, 'health_check', return_value=False):
                    server = TaskMCPServer()
                    
                    # Verify server still initializes but reports unhealthy database
                    server_info = server.get_server_info()
                    assert server_info['database_healthy'] is False
    
    def test_tool_registration_framework_ready(self):
        """Test that tool registration framework is ready (tools to be implemented later)."""
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None):
                with patch.object(DatabaseLayer, 'health_check', return_value=True):
                    server = TaskMCPServer()
                    
                    # Verify server initializes without errors
                    assert server is not None
                    
                    # Verify tools_registered count is 0 (tools not implemented yet)
                    server_info = server.get_server_info()
                    assert server_info['tools_registered'] == 0
    
    def test_setup_logging_configuration(self):
        """Test that logging is configured correctly."""
        with patch('logging.basicConfig') as mock_basic_config:
            setup_logging()
            
            # Verify logging was configured
            mock_basic_config.assert_called_once()
            
            # Verify the call included proper format and level
            call_args = mock_basic_config.call_args
            assert 'level' in call_args.kwargs
            assert 'format' in call_args.kwargs
            assert "%(asctime)s - %(name)s - %(levelname)s - %(message)s" in call_args.kwargs['format']
    
    @pytest.mark.asyncio
    async def test_server_run_with_database_connection_failure(self):
        """Test that server startup fails gracefully when database connection fails."""
        test_db_url = "sqlite:///test.db"
        
        with patch.dict(os.environ, {'DATABASE_URL': test_db_url}):
            with patch.object(DatabaseLayer, '__init__', return_value=None):
                with patch.object(DatabaseLayer, 'health_check', return_value=False):
                    with patch('src.config.validate_settings'):
                        server = TaskMCPServer()
                        
                        # Server run should raise RuntimeError for database connection failure
                        with pytest.raises(RuntimeError, match="Database connection failed"):
                            await server.run()
    
    def test_server_configuration_validation_error(self):
        """Test that validation function works correctly."""
        # Test the validation function directly by creating a settings instance with None database_url
        from src.config import Settings
        
        # Create a settings instance with no database_url
        test_settings = Settings(database_url=None)
        
        # Patch the global settings to use our test instance
        with patch('src.config.settings', test_settings):
            from src.config import validate_settings
            
            # Should raise ValueError for missing DATABASE_URL
            with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
                validate_settings()