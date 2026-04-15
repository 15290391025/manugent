"""MES Connector Base Class.

Abstract interface that all MES connectors must implement.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MESConnectionConfig:
    """Configuration for MES connection."""
    mes_type: str
    base_url: str
    auth_type: str = "bearer"  # bearer | basic | api_key | none
    auth_token: str = ""
    auth_username: str = ""
    auth_password: str = ""
    timeout: int = 30
    max_retries: int = 3
    rate_limit: int = 100  # requests per minute
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    """Standard result from MES queries."""
    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
        }


class MESConnector(ABC):
    """Abstract base class for MES connectors.

    All MES connectors must implement these methods to provide
    a consistent interface for agent tool calls.

    Example:
        >>> config = MESConnectionConfig(
        ...     mes_type="rest",
        ...     base_url="http://mes.local/api",
        ...     auth_token="xxx",
        ... )
        >>> connector = RestConnector(config)
        >>> await connector.connect()
        >>> result = await connector.execute_tool("query_production_data", {
        ...     "line_id": "SMT-03",
        ...     "metric": "oee",
        ...     "time_range": "today",
        ... })
    """

    def __init__(self, config: MESConnectionConfig) -> None:
        self.config = config
        self._connected = False
        self._schema: dict[str, Any] | None = None

    @property
    def mes_type(self) -> str:
        return self.config.mes_type

    @property
    def is_connected(self) -> bool:
        return self._connected

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to MES."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to MES."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify MES connection is alive."""
        ...

    @abstractmethod
    async def execute_tool(self, tool_name: str, params: dict[str, Any]) -> QueryResult:
        """Execute an MCP tool against the MES.

        Args:
            tool_name: Name of the MCP tool to execute.
            params: Parameters for the tool.

        Returns:
            QueryResult with data or error.
        """
        ...

    @abstractmethod
    async def get_schema(self) -> dict[str, Any]:
        """Return MES data schema for LLM context injection.

        This provides the LLM with information about what data
        is available in the MES system.
        """
        ...

    async def __aenter__(self) -> MESConnector:
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect()
