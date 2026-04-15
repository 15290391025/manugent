# ManuGent - 制造业智能Agent平台

> 给工厂MES系统装上AI大脑。用自然语言对话你的工厂。

---

## 一句话说明

ManuGent 是一个 **AI Agent 中间件**，连接你现有的MES系统和工厂人员。

它**不替代你的MES**，而是给MES加上：
- 自然语言交互（用说话代替点菜单）
- 智能监控和告警（AI帮你盯着产线）
- 根因分析（出问题了帮你找原因）
- 智能排产建议（多约束条件优化）

---

## 痛点 vs 解决方案

| 工厂真实痛点 | ManuGent怎么解决 |
|-------------|-----------------|
| 查个数据要开5个系统，导Excel分析半天 | "3号线最近一周良率怎么样？" 直接回答 |
| 良率下降了，排查半天找不到原因 | Agent自动关联设备/物料/人员/环境数据，秒级定位 |
| 新员工培训3个月才能用MES | 自然语言交互，小白也能查数据做分析 |
| 排产靠老师傅经验，换人就乱 | AI排产考虑所有约束，输出可执行方案 |
| 多工厂数据不通，总部看不到全貌 | Agent层统一接入各厂MES，一个界面管所有 |

---

## 目标用户

### 主要：大型电子制造企业
- **立讯精密** — AirPods/iPhone/Vision Pro组装，20万+员工
- **歌尔股份** — VR头显/声学器件
- **比亚迪电子** — 手机结构件/汽车零部件
- **富士康/鸿海** — 全球最大代工厂

这类企业特征：
- 已有MES系统（西门子/鼎捷/自研），投入几千万到几亿
- 几十条SMT产线，跨多个工厂
- 客户（Apple/汽车Tier1）对品质追溯要求极高
- 招工越来越难，自动化是刚需

### 次要：MES系统集成商
- 给客户交付MES项目时，需要AI增值模块
- 不想从零开发Agent能力，想用现成中间件

---

## 技术架构

详见 [ARCHITECTURE.md](docs/ARCHITECTURE.md)

```
用户层:  Chat / 仪表盘 / 移动端 / API
    │
Agent层:  查询Agent / 告警Agent / 排产Agent / 根因分析Agent
    │
协议层:  MCP Manufacturing Protocol (标准化Agent↔MES通信)
    │
连接层:  MES连接器 / ERP连接器 / 设备连接器(OPC UA/MQTT)
    │
数据层:  PostgreSQL + TimescaleDB / Redis
```

**关键设计原则：**
1. **非侵入式** — 只读优先，写操作需要人工确认
2. **ISA-95对齐** — 数据模型遵循工业标准
3. **边缘优先** — 支持本地LLM推理（工厂网络受限）
4. **多Agent协作** — 不同职责的专职Agent
5. **治理先行** — 审计日志、约束校验、人机协同

---

## 核心功能模块

### Module 1: MCP Manufacturing Protocol
为制造业定制的MCP扩展协议，定义Agent可调用的工具集：
- `query_production_data` — 查询生产数据
- `get_equipment_status` — 获取设备状态
- `get_quality_records` — 获取品质记录
- `analyze_root_cause` — 触发根因分析
- `suggest_schedule` — 排产建议（需人工确认）
- `create_work_order` — 创建工单（需人工确认）

### Module 2: MES Connector Framework
可插拔的MES连接器：
- **通用REST/GraphQL** — 任何有API的MES
- **西门子Opcenter** — 适配其API
- **鼎捷数智** — 国产MES #1
- **摩尔元数** — SMT专精MES
- **自研MES** — 提供适配模板

### Module 3: Agent Suite
专职Agent集合：
- **Query Agent** — 自然语言转MES查询
- **Alert Agent** — 实时监控 + 异常检测
- **RootCause Agent** — 多维度关联分析
- **Schedule Agent** — 约束满足排产优化

### Module 4: Edge Runtime
边缘端推理能力：
- Ollama/vLLM 本地推理
- 模型可选：Qwen2.5-72B / DeepSeek-V3 / Llama-3.3
- 离线模式：核心功能不依赖外网

---

## 开发路线图

详见 [ROADMAP.md](docs/ROADMAP.md)

**Phase 1 (Month 1-2): 基础搭建**
- MCP Manufacturing Protocol v0.1
- 通用REST MES连接器
- Query Agent（自然语言查MES）
- 基础Chat UI

**Phase 2 (Month 3-4): 智能增强**
- 多Agent编排（LangGraph）
- 告警Agent + 异常检测
- 根因分析Agent
- 西门子/鼎捷连接器

**Phase 3 (Month 5-6): 生产就绪**
- 排产Agent
- 边缘部署（Ollama集成）
- 权限管理 + 审计日志
- Docker一键部署

**Phase 4 (Month 7+): 生态建设**
- 连接器插件市场
- 多工厂联邦
- 企业级功能（SSO、多租户）

---

## 快速开始

```bash
# 克隆
git clone https://github.com/yourname/manugent.git
cd manugent

# 配置
cp configs/.env.example configs/.env
# 编辑 .env 填入MES连接信息和LLM API Key

# Docker启动
docker compose up -d

# 或本地运行
pip install -e .
manugent serve --config configs/default.yaml
```

```python
from manugent import MESAgent

agent = MESAgent(
    mes_type="custom",
    mes_url="http://your-mes.internal/api",
    llm_provider="openai",
)

# 自然语言查询
response = agent.chat("3号线今天OEE是多少？")

# 结构化分析
result = agent.analyze(
    "分析最近7天良率下降的原因",
    context={"line": "SMT-03", "time_range": "7d"}
)
```

---

## 竞品对比

| 维度 | ManuGent | 西门子+AI | 鼎捷+AI | 开源方案 |
|------|----------|----------|---------|---------|
| 开源 | ✅ MIT | ❌ | ❌ | 部分 |
| MES无关 | ✅ 对接任意MES | 绑定Opcenter | 绑定鼎捷 | 大多绑定 |
| Agent架构 | ✅ 多Agent | 单模型 | 单模型 | 少见 |
| 边缘部署 | ✅ Ollama | ❌ 云端 | ❌ | 少见 |
| ISA-95 | ✅ | ✅ | 部分 | ❌ |
| 中文原生 | ✅ | ❌ | ✅ | 少见 |
| 价格 | 免费 | 百万+ | 百万+ | 免费 |

---

## 参与贡献

我们需要：
- **制造行业专家** — 帮助定义需求、验证方案
- **AI/LLM工程师** — 构建更好的Agent和推理链
- **MES开发者** — 开发更多MES连接器
- **工厂一线人员** — 告诉我们你的真实痛点

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 致谢

- [Digital Twin Consortium](https://www.digitaltwinconsortium.org/) — 工业AI Agent宣言
- [MCP Protocol](https://modelcontextprotocol.io/) — 标准化Agent-工具通信
- AWS [industrial-data-store](https://github.com/aws-samples/industrial-data-store-simulation-chatbot) — MES聊天机器人参考架构
- 所有开源MES项目

---

## License

MIT
