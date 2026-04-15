# ManuGent - Manufacturing Intelligence Agent

> 给工厂MES系统装上AI大脑。用自然语言对话你的工厂。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/downloads/)
[![Status: Planning](https://img.shields.io/badge/status-planning-orange.svg)](https://github.com/15290391025/manugent)

[English](README.md) | [中文](README_zh.md)

---

## What is ManuGent?

ManuGent is an **AI Agent middleware layer** that sits between your existing MES system and your factory staff. It does NOT replace your MES — it gives it a brain.

**Before ManuGent:**
> 工程师: 打开MES → 筛选产线 → 选日期 → 导出报表 → Excel分析 → 写报告 → 汇报

**With ManuGent:**
> 工程师: "3号线最近一周良率下降的原因是什么？"
> ManuGent: 分析数据 → 关联事件 → 给出根因 → 建议措施

---

## Why ManuGent?

| Problem | ManuGent Solution |
|---------|-------------------|
| MES数据需要手动查询导出 | 自然语言直接问，秒级响应 |
| 异常靠人工经验判断 | AI Agent实时监控+根因分析 |
| 多系统数据孤岛 | 统一Agent层打通MES/ERP/QMS |
| 排产靠Excel拍脑袋 | 智能排产建议，约束满足优化 |
| 培训新员工周期长 | AI助手降低MES使用门槛 |

---

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │         User Interfaces             │
                    │   Chat │ Dashboard │ Mobile │ API    │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │       Agent Orchestration           │
                    │  (LangGraph / CrewAI / AutoGen)     │
                    │                                     │
                    │  ┌───────┐ ┌───────┐ ┌───────────┐ │
                    │  │Query  │ │Alert  │ │Schedule   │ │
                    │  │Agent  │ │Agent  │ │Agent      │ │
                    │  └───┬───┘ └───┬───┘ └─────┬─────┘ │
                    │      └─────────┼───────────┘       │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │      MCP Manufacturing Protocol     │
                    │  (Standardized Agent ↔ MES Bridge)  │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
    ┌─────▼─────┐          ┌──────▼──────┐          ┌──────▼──────┐
    │ MES       │          │ ERP         │          │ QMS/WMS/SCADA│
    │ Connector │          │ Connector   │          │ Connector    │
    │           │          │             │          │              │
    │ Siemens   │          │ SAP         │          │ OPC UA       │
    │ 鼎捷      │          │ Oracle      │          │ MQTT         │
    │ 摩尔元数   │          │ 用友/金蝶    │          │ Modbus       │
    │ 自研MES   │          │             │          │ REST/GraphQL │
    └───────────┘          └─────────────┘          └──────────────┘
```

### Key Design Principles

1. **Non-invasive**: Read-heavy first, write operations require explicit approval
2. **ISA-95 Compliant**: Data models follow ISA-95/Purdue model standards
3. **Edge-First**: Local LLM inference (Ollama/vLLM) with cloud fallback
4. **Multi-Agent**: Specialized agents for different concerns (query, alert, schedule)
5. **Governance-First**: Audit trail, constraint validation, human-in-the-loop

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Agent Framework | LangGraph | Stateful multi-step reasoning, production-grade |
| LLM Backend | OpenAI / Claude / Qwen / Local (Ollama) | Flexibility, can run offline |
| Data Protocol | MCP (Model Context Protocol) | Standardized tool calling |
| OT Connectors | OPC UA / MQTT | Industry standard IoT protocols |
| Backend API | FastAPI (Python) | Async, fast, great for data pipelines |
| Database | PostgreSQL + TimescaleDB | Relational + time-series for sensor data |
| Cache | Redis | Real-time state, pub/sub |
| Edge Runtime | Ollama / vLLM | On-premise LLM inference |
| Frontend | React + shadcn/ui | Chat interface + dashboards |

---

## Quick Start

```bash
# Clone
git clone https://github.com/yourname/manugent.git
cd manugent

# Setup
cp configs/.env.example configs/.env
# Edit .env with your MES connection and LLM API keys

# Run with Docker
docker compose up -d

# Or run locally
pip install -e .
manugent serve --config configs/default.yaml
```

### Connect to your MES

```python
from manugent import MESAgent

agent = MESAgent(
    mes_type="siemens_opcenter",  # or "dingjie", "custom"
    mes_url="https://your-mes.example.com/api",
    llm_provider="openai",       # or "ollama" for local
)

# Natural language query
response = agent.chat("3号线今天OEE是多少？")
print(response)

# Structured query
result = agent.query(
    "Show me all failed batches in the last 24 hours "
    "with root cause analysis"
)
```

---

## Use Cases

### Tier 1: Natural Language MES Query (MVP)
- "3号线最近一周的良率趋势"
- "今天有哪些设备需要保养？"
- "昨天夜班的产量为什么比白班低？"
- 自动生成每日生产晨会报告

### Tier 2: Intelligent Monitoring & Alerting
- 实时异常检测（传感器数据 + 生产指标）
- 良率波动根因分析（关联设备、物料、人员、环境）
- 预测性维护建议（基于设备运行数据趋势）

### Tier 3: Autonomous Operations
- 多约束条件下的智能排产
- 动态人员排班（技能匹配 + 负荷均衡）
- 物料需求预测与采购建议

### Tier 4: Cognitive Manufacturing (Roadmap)
- 跨工厂知识迁移
- 自适应工艺参数优化
- 合规自动化（客户审核、体系认证）

---

## Who Should Use This?

- **大型电子制造企业** (立讯精密、歌尔股份、比亚迪电子...)
  - 已有MES系统，需要AI增强
  - 多工厂、多产线协同需求
  - 客户（Apple/汽车）品质追溯要求高

- **MES系统集成商/ISV**
  - 给客户提供AI增值模块
  - 不想从零开发Agent能力

- **智能制造研究机构**
  - 探索LLM在工业场景的落地

---

## Roadmap

See [ROADMAP.md](docs/ROADMAP.md) for detailed timeline.

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| Phase 1: Foundation | Month 1-2 | Core protocol, one MES connector, basic chat agent |
| Phase 2: Intelligence | Month 3-4 | Multi-agent system, alerting, root cause analysis |
| Phase 3: Operations | Month 5-6 | Scheduling agent, edge deployment, production-ready |
| Phase 4: Ecosystem | Month 7+ | Plugin marketplace, multi-MES federation, enterprise features |

---

## Contributing

We welcome contributors from:
- **Manufacturing domain experts** — help us define requirements and validate solutions
- **LLM/AI engineers** — build better agents and reasoning chains
- **MES developers** — create connectors for more MES platforms
- **Factory floor workers** — tell us what actually sucks about your MES

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — use it however you want.

---

## Acknowledgments

- [Digital Twin Consortium](https://www.digitaltwinconsortium.org/) — Industrial AI Agent Manifesto
- [MCP Protocol](https://modelcontextprotocol.io/) — Standardized agent-tool communication
- AWS [industrial-data-store-simulation-chatbot](https://github.com/aws-samples/industrial-data-store-simulation-chatbot) — Reference architecture for MES chatbot
- All open-source MES projects that inspire this work
