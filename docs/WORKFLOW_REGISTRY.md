# Workflow Registry

ManuGent 现在把制造诊断能力抽象为可注册的 workflow，而不是把 API 固定死在单个 RCA 场景上。

## 目标

- 让前端、API、CLI 可以发现当前系统有哪些制造 workflow。
- 让新增 workflow 不需要新增一套路由。
- 让每个 workflow 明确声明输入参数、证据类型、输出类型和别名。

## API

列出 workflow：

```bash
curl http://localhost:8000/workflows
```

运行 workflow：

```bash
curl -X POST http://localhost:8000/workflows/yield_drop/run \
  -H "Content-Type: application/json" \
  -d '{"params":{"line_id":"SMT-03","time_range":"24h"},"session_id":"demo"}'
```

返回结构：

```json
{
  "workflow_id": "root_cause.yield_drop",
  "status": "completed",
  "result": {
    "incident_type": "yield_drop",
    "line_id": "SMT-03",
    "finding": "...",
    "confidence": 0.83,
    "evidence": [],
    "recommendations": []
  }
}
```

## 当前内置 Workflow

| workflow_id | aliases | 说明 |
|-------------|---------|------|
| `root_cause.yield_drop` | `yield_drop`, `yield-drop`, `root_cause_yield_drop` | 良率下降根因分析 |

## 扩展方式

新增 workflow 时需要提供：

- `workflow_id`
- `name`
- `description`
- `parameters`
- `evidence_types`
- `factory`
- `runner`

核心注册入口在：

```text
src/manugent/workflows/registry.py
```

这个设计的重点是：workflow 的业务编排留在 Python 代码中，API 只负责发现、校验参数和运行。这样更适合后续加入 `wip_bottleneck`、`equipment_failure`、`quality_anomaly` 等制造诊断能力。
