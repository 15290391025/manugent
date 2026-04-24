"""Demo: LangGraph-orchestrated root-cause workflow.

Run from the repository root:
    PYTHONPATH=src python3 examples/demo_langgraph_root_cause.py
"""

from __future__ import annotations

import asyncio

from manugent.connector.demo import DemoMESConnector
from manugent.memory import InMemoryMemoryStore
from manugent.memory.recipes import remember_incident
from manugent.workflows import LangGraphRootCauseWorkflow


async def main() -> None:
    memory = InMemoryMemoryStore()
    remember_incident(
        memory,
        "Previous SMT-03 yield drop was resolved by cleaning MOUNTER-03A nozzle bank.",
        scope="demo-factory",
        tags=["SMT-03", "yield", "MOUNTER-03A"],
        confidence=0.84,
    )

    connector = DemoMESConnector()
    await connector.connect()

    workflow = LangGraphRootCauseWorkflow(
        connector,
        memory_store=memory,
        memory_scope="demo-factory",
    )
    report = await workflow.analyze_yield_drop("SMT-03", "24h")

    print("# LangGraph Root Cause Workflow Report")
    print(f"Graph steps: {' -> '.join(workflow.last_steps)}")
    print(f"Finding: {report.finding}")
    print(f"Confidence: {report.confidence}")
    print()
    print("## Evidence Chain")
    for item in report.evidence:
        print(f"- [{item.evidence_type.value}] {item.summary}")
    print()
    print("## Recommended Actions")
    for item in report.recommendations:
        approval = "approval boundary" if item.requires_approval else "advisory"
        print(f"- ({approval}) {item.action}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as exc:
        if "LangGraph is required" not in str(exc):
            raise
        print(exc)
