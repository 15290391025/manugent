"""ManuGent - Manufacturing Intelligence Agent Platform.

Give your factory MES a brain. AI Agent middleware that connects
to existing MES systems and provides natural language interaction,
intelligent monitoring, root cause analysis, and smart scheduling.

Example:
    >>> from manugent import MESAgent
    >>> agent = MESAgent(mes_type="rest", mes_url="http://mes.local/api")
    >>> response = agent.chat("3号线今天OEE是多少？")
"""

__version__ = "0.1.0"

from manugent.agent.core import MESAgent
from manugent.connector.base import MESConnector

__all__ = ["MESAgent", "MESConnector", "__version__"]
