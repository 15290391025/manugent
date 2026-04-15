"""MCP Manufacturing Protocol - Tool definitions for agent-MES communication.

This module defines the standardized tool interface between LLM agents
and Manufacturing Execution Systems, based on the Model Context Protocol
with manufacturing-specific extensions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolCategory(str, Enum):
    """Categories of manufacturing tools."""
    PRODUCTION = "production"
    EQUIPMENT = "equipment"
    QUALITY = "quality"
    ANALYSIS = "analysis"
    ACTION = "action"


class SafetyLevel(str, Enum):
    """Safety classification for tool operations."""
    READ_ONLY = "read_only"           # Auto-approved
    ADVISORY = "advisory"             # Returns suggestions, no execution
    APPROVAL_REQUIRED = "approval"    # Requires human approval
    RESTRICTED = "restricted"         # Admin only


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    type: str  # "string", "integer", "float", "boolean", "enum", "array", "object"
    description: str
    required: bool = False
    default: Any = None
    enum_values: list[str] | None = None


@dataclass
class MCPTool:
    """Definition of a manufacturing MCP tool."""
    name: str
    description: str
    category: ToolCategory
    safety_level: SafetyLevel
    parameters: list[ToolParameter] = field(default_factory=list)
    returns: str = "dict"
    examples: list[str] = field(default_factory=list)


# ============================================
# Manufacturing Tool Registry
# ============================================

MANUFACTURING_TOOLS: dict[str, MCPTool] = {}


def register_tool(tool: MCPTool) -> None:
    """Register a manufacturing tool."""
    MANUFACTURING_TOOLS[tool.name] = tool


def get_tool(name: str) -> MCPTool | None:
    """Get a tool by name."""
    return MANUFACTURING_TOOLS.get(name)


def list_tools(
    category: ToolCategory | None = None,
    safety_level: SafetyLevel | None = None,
) -> list[MCPTool]:
    """List registered tools, optionally filtered."""
    tools = list(MANUFACTURING_TOOLS.values())
    if category:
        tools = [t for t in tools if t.category == category]
    if safety_level:
        tools = [t for t in tools if t.safety_level == safety_level]
    return tools


# ============================================
# Register Built-in Tools
# ============================================

# --- Production Query Tools ---

register_tool(MCPTool(
    name="query_production_data",
    description="查询生产指标数据，包括OEE、良率、产量、节拍时间等",
    category=ToolCategory.PRODUCTION,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("line_id", "string", "产线ID，如 'SMT-03'", required=True),
        ToolParameter("metric", "enum", "查询指标", required=True,
                      enum_values=["oee", "yield", "output", "cycle_time", "throughput"]),
        ToolParameter("time_range", "string", "时间范围，如 'today', 'yesterday', '7d', '2024-01-01~2024-01-07'",
                      default="today"),
        ToolParameter("granularity", "enum", "数据粒度",
                      enum_values=["raw", "hourly", "shift", "daily"], default="hourly"),
    ],
    returns="timeseries_data",
    examples=[
        "query_production_data(line_id='SMT-03', metric='oee', time_range='today')",
        "query_production_data(line_id='ASM-01', metric='yield', time_range='7d', granularity='daily')",
    ],
))

register_tool(MCPTool(
    name="query_wip",
    description="查询在制品(WIP)状态，查看各工位的在产情况",
    category=ToolCategory.PRODUCTION,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("line_id", "string", "产线ID"),
        ToolParameter("product_id", "string", "产品ID"),
        ToolParameter("station", "string", "工位"),
    ],
    returns="wip_list",
))

register_tool(MCPTool(
    name="query_production_orders",
    description="查询生产工单状态",
    category=ToolCategory.PRODUCTION,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("order_id", "string", "工单ID"),
        ToolParameter("status", "enum", "工单状态",
                      enum_values=["pending", "in_progress", "completed", "on_hold"]),
        ToolParameter("time_range", "string", "时间范围", default="today"),
    ],
    returns="order_list",
))

# --- Equipment Tools ---

register_tool(MCPTool(
    name="get_equipment_status",
    description="获取设备实时状态",
    category=ToolCategory.EQUIPMENT,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("equipment_id", "string", "设备ID", required=True),
    ],
    returns="equipment_status",
    examples=["get_equipment_status(equipment_id='RFW-SMT-02')"],
))

register_tool(MCPTool(
    name="get_equipment_history",
    description="获取设备历史告警和维护记录",
    category=ToolCategory.EQUIPMENT,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("equipment_id", "string", "设备ID", required=True),
        ToolParameter("days", "integer", "查询天数", default=30),
    ],
    returns="event_list",
))

# --- Quality Tools ---

register_tool(MCPTool(
    name="get_quality_records",
    description="查询品质检验记录",
    category=ToolCategory.QUALITY,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("line_id", "string", "产线ID"),
        ToolParameter("defect_type", "string", "不良类型"),
        ToolParameter("time_range", "string", "时间范围", default="24h"),
    ],
    returns="quality_records",
))

register_tool(MCPTool(
    name="get_traceability",
    description="获取产品全链路追溯信息",
    category=ToolCategory.QUALITY,
    safety_level=SafetyLevel.READ_ONLY,
    parameters=[
        ToolParameter("serial_number", "string", "产品序列号", required=True),
    ],
    returns="traceability_chain",
    examples=["get_traceability(serial_number='SN2026041500001')"],
))

# --- Analysis Tools ---

register_tool(MCPTool(
    name="analyze_root_cause",
    description="触发根因分析，分析品质或设备异常的根本原因",
    category=ToolCategory.ANALYSIS,
    safety_level=SafetyLevel.ADVISORY,
    parameters=[
        ToolParameter("issue_type", "enum", "问题类型", required=True,
                      enum_values=["yield_drop", "equipment_failure", "quality_anomaly", "throughput_decline"]),
        ToolParameter("context", "object", "上下文信息（产线、时间范围、相关指标等）"),
    ],
    returns="root_cause_report",
    examples=["analyze_root_cause(issue_type='yield_drop', context={'line': 'SMT-05', 'time_range': '3d'})"],
))

# --- Action Tools (require human approval) ---

register_tool(MCPTool(
    name="suggest_schedule",
    description="生成优化的生产排程建议",
    category=ToolCategory.ACTION,
    safety_level=SafetyLevel.APPROVAL_REQUIRED,
    parameters=[
        ToolParameter("line_ids", "array", "产线ID列表", required=True),
        ToolParameter("horizon", "string", "排程时间范围", default="24h"),
        ToolParameter("constraints", "object", "约束条件（交期、物料、人员等）"),
    ],
    returns="schedule_proposal",
))

register_tool(MCPTool(
    name="create_alert",
    description="创建告警/通知",
    category=ToolCategory.ACTION,
    safety_level=SafetyLevel.APPROVAL_REQUIRED,
    parameters=[
        ToolParameter("severity", "enum", "严重级别", required=True,
                      enum_values=["info", "warning", "critical"]),
        ToolParameter("message", "string", "告警消息", required=True),
        ToolParameter("assignee", "string", "指派给"),
    ],
    returns="alert_id",
))
