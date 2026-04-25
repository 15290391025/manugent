"""Workflow registry for manufacturing diagnostics."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from manugent.connector.base import MESConnector
from manugent.memory import MemoryStore
from manugent.models import IncidentReport
from manugent.workflows.root_cause import RootCauseWorkflow

WorkflowFactory = Callable[[MESConnector, MemoryStore | None, str], Any]


@dataclass(frozen=True)
class WorkflowParameter:
    """Input parameter exposed by a workflow."""

    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-serializable parameter metadata."""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required,
            "default": self.default,
        }


@dataclass(frozen=True)
class WorkflowDefinition:
    """Metadata and executor binding for a workflow."""

    workflow_id: str
    name: str
    description: str
    category: str
    parameters: list[WorkflowParameter]
    evidence_types: list[str]
    output_type: str
    factory: WorkflowFactory
    runner: str
    aliases: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return public workflow metadata."""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
            "evidence_types": self.evidence_types,
            "output_type": self.output_type,
            "aliases": self.aliases,
        }


class WorkflowRegistry:
    """Registry and runner for manufacturing workflows."""

    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._aliases: dict[str, str] = {}

    def register(self, definition: WorkflowDefinition) -> None:
        """Register one workflow definition."""
        self._workflows[definition.workflow_id] = definition
        for alias in definition.aliases:
            self._aliases[alias] = definition.workflow_id

    def list(self) -> list[WorkflowDefinition]:
        """List workflow definitions in stable order."""
        return [self._workflows[key] for key in sorted(self._workflows)]

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        """Resolve a workflow by ID or alias."""
        normalized = workflow_id.replace("-", "_")
        resolved_id = self._aliases.get(workflow_id) or self._aliases.get(normalized)
        return self._workflows.get(resolved_id or workflow_id) or self._workflows.get(normalized)

    async def run(
        self,
        workflow_id: str,
        connector: MESConnector,
        params: dict[str, Any],
        *,
        memory_store: MemoryStore | None = None,
        memory_scope: str = "default",
    ) -> IncidentReport:
        """Run a registered workflow and return its structured report."""
        definition = self.get(workflow_id)
        if definition is None:
            raise KeyError(f"Unknown workflow: {workflow_id}")

        resolved_params = self._resolve_params(definition, params)
        workflow = definition.factory(connector, memory_store, memory_scope)
        runner = getattr(workflow, definition.runner)
        result = runner(**resolved_params)
        if isinstance(result, Awaitable):
            return await result
        return result

    def _resolve_params(
        self,
        definition: WorkflowDefinition,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        resolved: dict[str, Any] = {}
        for parameter in definition.parameters:
            if parameter.name in params:
                resolved[parameter.name] = params[parameter.name]
            elif parameter.required and parameter.default is None:
                raise ValueError(
                    f"Missing required parameter '{parameter.name}' "
                    f"for workflow '{definition.workflow_id}'"
                )
            else:
                resolved[parameter.name] = parameter.default
        return resolved


def _root_cause_factory(
    connector: MESConnector,
    memory_store: MemoryStore | None,
    memory_scope: str,
) -> RootCauseWorkflow:
    return RootCauseWorkflow(
        connector=connector,
        memory_store=memory_store,
        memory_scope=memory_scope,
    )


def create_default_workflow_registry() -> WorkflowRegistry:
    """Create the built-in manufacturing workflow registry."""
    registry = WorkflowRegistry()
    registry.register(
        WorkflowDefinition(
            workflow_id="root_cause.yield_drop",
            name="良率下降根因分析",
            description="关联生产、质量、物料、设备和历史记忆，生成良率下降 RCA 报告。",
            category="root_cause",
            parameters=[
                WorkflowParameter("line_id", "string", "产线 ID，例如 SMT-03"),
                WorkflowParameter(
                    "time_range",
                    "string",
                    "分析时间范围，例如 24h、7d、today",
                    required=False,
                    default="24h",
                ),
            ],
            evidence_types=["production", "quality", "material", "equipment", "memory"],
            output_type="incident_report",
            factory=_root_cause_factory,
            runner="analyze_yield_drop",
            aliases=["yield_drop", "yield-drop", "root_cause_yield_drop"],
        )
    )
    return registry
