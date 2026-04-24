# Root Cause Workflow

The root-cause workflow is the most important ManuGent demo because it shows
how MES data and Agent reasoning combine into an evidence chain.

## Goal

Answer questions like:

```text
SMT-03 最近 24 小时良率为什么下降？
```

The workflow does not rely on the LLM guessing which data matters. It executes a
deterministic manufacturing analysis path and produces structured evidence that
an LLM, UI, or human engineer can review.

## Workflow Steps

```text
yield drop question
→ query yield trend
→ query quality defects
→ infer related equipment
→ query equipment history
→ retrieve historical incident memory
→ build evidence chain
→ score confidence
→ produce recommended actions
```

Implemented in:

```text
src/manugent/workflows/root_cause.py
src/manugent/workflows/langgraph_root_cause.py
```

Run:

```bash
PYTHONPATH=src python3 examples/demo_workflow_root_cause.py
PYTHONPATH=src python3 examples/demo_langgraph_root_cause.py
```

## LangGraph Orchestration

The deterministic workflow remains the business baseline. The LangGraph version
wraps the same MES analysis into explicit nodes:

```text
query_production
→ query_quality
→ query_equipment
→ build_evidence
→ build_report
```

This is useful because a manufacturing Agent workflow should make state
transitions visible. Each node has a narrow responsibility, passes structured
state forward, and can later be replaced with a richer implementation:

- `query_production`: read yield trend from MES
- `query_quality`: read defect records and quality summary
- `query_equipment`: infer equipment and load alarm history
- `build_evidence`: convert raw data into typed evidence
- `build_report`: score confidence and produce recommended actions

The graph is intentionally not an approval engine. Human approval in factories
is normally owned by MES, BPM, Lark/Feishu, ServiceNow, or a custom internal
system. ManuGent marks actions that cross the safety boundary; the enterprise
workflow system should decide how approval is routed and executed.

## Evidence Chain

Each evidence item has:

- `type`: production, quality, material, equipment, traceability, or memory
- `summary`: human-readable finding
- `source_tool`: which tool produced the data
- `confidence`: local confidence for this evidence
- `data`: supporting structured payload

Example:

```text
[production] Yield is 92.4%, trend=down, average=95.56%.
[quality] Top defect is solder_bridge with 3 records.
[material] Defects concentrate on material lot SP-20260424-A.
[equipment] MOUNTER-03A has warning events.
[memory] Previous SMT-03 yield drop was resolved by cleaning nozzle bank.
```

## Why This Matters

This workflow demonstrates key MES + Agent principles:

- Agent reasoning should be tool-grounded, not free-form speculation.
- Manufacturing RCA requires correlating production, quality, material, and equipment data.
- Historical incidents should influence current analysis but remain separate evidence.
- Recommendations must show ownership and whether they cross an approval boundary.
- Outputs should be structured enough for dashboards, audit logs, and follow-up workflows.

## Current Limitations

- Equipment inference is heuristic: `SMT-03` maps to `MOUNTER-03A`.
- Correlation is deterministic and demo-oriented, not statistical.
- It does not yet persist incident reports after analysis.
- LangGraph orchestration is linear today; no conditional routing is implemented yet.

## Next Extensions

- Add time-window overlap scoring between alarms and defect spikes
- Add material-lot comparison against baseline lots
- Persist `IncidentReport` into memory and audit storage
- Add conditional routing for missing evidence or low-confidence reports
- Use the RCA graph as one node in a larger supervisor-style Agent workflow
