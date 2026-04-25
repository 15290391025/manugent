"""LangGraph orchestration for manufacturing root-cause analysis."""

from __future__ import annotations

from typing import Any, TypedDict

from manugent.connector.base import MESConnector
from manugent.memory import MemoryStore
from manugent.models import Evidence, IncidentReport
from manugent.workflows.root_cause import RootCauseWorkflow


class RootCauseGraphState(TypedDict, total=False):
    """State passed between RCA graph nodes."""

    line_id: str
    time_range: str
    equipment_id: str
    yield_data: dict[str, Any]
    quality_data: dict[str, Any]
    equipment_history: list[dict[str, Any]]
    evidence: list[Evidence]
    report: IncidentReport
    steps: list[str]


class LangGraphRootCauseWorkflow:
    """Run the RCA workflow as explicit LangGraph nodes.

    The graph keeps MES orchestration deterministic while exposing each
    manufacturing reasoning step as a node that can later be routed, observed,
    retried, or extended with multi-agent handoffs.
    """

    def __init__(
        self,
        connector: MESConnector,
        memory_store: MemoryStore | None = None,
        memory_scope: str = "default",
    ) -> None:
        self.base_workflow = RootCauseWorkflow(
            connector=connector,
            memory_store=memory_store,
            memory_scope=memory_scope,
        )
        self.last_steps: list[str] = []
        self._graph = None

    async def analyze_yield_drop(
        self,
        line_id: str,
        time_range: str = "24h",
    ) -> IncidentReport:
        """Analyze a yield drop through a LangGraph state machine."""
        graph = self._get_graph()
        final_state = await graph.ainvoke(
            {
                "line_id": line_id,
                "time_range": time_range,
                "steps": [],
            }
        )
        self.last_steps = final_state.get("steps", [])
        return final_state["report"]

    def _get_graph(self):
        if self._graph is None:
            self._graph = self._build_graph()
        return self._graph

    def _build_graph(self):
        try:
            from langgraph.graph import END, StateGraph
        except ModuleNotFoundError as exc:  # pragma: no cover - dependency guard
            raise RuntimeError(
                "LangGraph is required for LangGraphRootCauseWorkflow. "
                "Install project dependencies with `pip install -e .`."
            ) from exc

        workflow = StateGraph(RootCauseGraphState)
        workflow.add_node("query_production", self._query_production)
        workflow.add_node("query_quality", self._query_quality)
        workflow.add_node("query_equipment", self._query_equipment)
        workflow.add_node("build_evidence", self._build_evidence)
        workflow.add_node("build_report", self._build_report)

        workflow.set_entry_point("query_production")
        workflow.add_edge("query_production", "query_quality")
        workflow.add_edge("query_quality", "query_equipment")
        workflow.add_edge("query_equipment", "build_evidence")
        workflow.add_edge("build_evidence", "build_report")
        workflow.add_edge("build_report", END)
        return workflow.compile()

    async def _query_production(self, state: RootCauseGraphState) -> RootCauseGraphState:
        yield_data = await self.base_workflow._require_tool(
            "query_production_data",
            {
                "line_id": state["line_id"],
                "metric": "yield",
                "time_range": state["time_range"],
            },
        )
        return {
            "yield_data": yield_data,
            "steps": [*state.get("steps", []), "query_production"],
        }

    async def _query_quality(self, state: RootCauseGraphState) -> RootCauseGraphState:
        quality_data = await self.base_workflow._require_tool(
            "get_quality_records",
            {
                "line_id": state["line_id"],
                "time_range": state["time_range"],
            },
        )
        return {
            "quality_data": quality_data,
            "steps": [*state.get("steps", []), "query_quality"],
        }

    async def _query_equipment(self, state: RootCauseGraphState) -> RootCauseGraphState:
        equipment_id = self.base_workflow._infer_equipment_id(state["line_id"])
        equipment_history = await self.base_workflow._require_tool(
            "get_equipment_history",
            {"equipment_id": equipment_id, "days": 7},
        )
        return {
            "equipment_id": equipment_id,
            "equipment_history": equipment_history,
            "steps": [*state.get("steps", []), "query_equipment"],
        }

    async def _build_evidence(self, state: RootCauseGraphState) -> RootCauseGraphState:
        evidence = [
            self.base_workflow._production_evidence(state["yield_data"]),
            self.base_workflow._quality_evidence(state["quality_data"]),
            self.base_workflow._material_evidence(state["quality_data"]),
            self.base_workflow._equipment_evidence(
                state["equipment_id"],
                state["equipment_history"],
            ),
        ]
        evidence.extend(self.base_workflow._memory_evidence(state["line_id"]))
        return {
            "evidence": evidence,
            "steps": [*state.get("steps", []), "build_evidence"],
        }

    async def _build_report(self, state: RootCauseGraphState) -> RootCauseGraphState:
        evidence = state["evidence"]
        report = IncidentReport(
            incident_type="yield_drop",
            line_id=state["line_id"],
            finding=self.base_workflow._build_finding(evidence),
            confidence=self.base_workflow._score_confidence(evidence),
            evidence=evidence,
            recommendations=self.base_workflow._recommend_actions(evidence),
        )
        self.base_workflow._persist_report(report)
        return {
            "report": report,
            "steps": [*state.get("steps", []), "build_report"],
        }
