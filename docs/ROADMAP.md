# ManuGent Roadmap

## Phase 1: Foundation (Month 1-2)

**Goal: 用自然语言查MES数据**

### Deliverables
- [ ] MCP Manufacturing Protocol v0.1 定义
- [ ] 通用 REST MES 连接器
- [ ] Query Agent (自然语言 → MES查询)
- [ ] 基础 Chat UI (React)
- [ ] FastAPI 后端骨架
- [ ] Docker Compose 一键部署
- [ ] 配置文档 + 使用示例

### Technical Tasks
- [ ] 定义 MCP Manufacturing Tool Schema (YAML)
- [ ] 实现 `query_production_data`, `get_equipment_status`, `get_quality_records`
- [ ] REST 连接器 + 字段映射配置
- [ ] LangGraph 单Agent workflow (understand → query → format)
- [ ] Text-to-API 转换（LLM将自然语言映射到MCP工具调用）
- [ ] Chat UI: 消息列表 + 输入框 + 数据卡片展示
- [ ] 本地 SQLite 存储查询历史
- [ ] Ollama 集成（本地推理可选）

### Success Criteria
- 用户输入 "3号线今天OEE是多少" 能在5秒内返回正确结果
- 支持至少10种常见MES查询意图
- Docker compose 3步内启动完成

---

## Phase 2: Intelligence (Month 3-4)

**Goal: 实时监控 + 异常检测 + 根因分析**

### Deliverables
- [ ] 多Agent编排 (LangGraph)
- [ ] Alert Agent (实时监控告警)
- [ ] RootCause Agent (根因分析)
- [ ] 西门子 Opcenter 连接器
- [ ] 鼎捷 MES 连接器
- [ ] 告警Dashboard
- [ ] MQTT/OPC UA 基础接入

### Technical Tasks
- [ ] LangGraph 多Agent路由 (Supervisor pattern)
- [ ] Alert Agent: 基于规则 + LLM 的异常检测
- [ ] RootCause Agent: 关联分析 workflow
  - 时间关联（设备告警 → 良率下降）
  - 物料关联（同批次物料 → 多线异常）
  - 人员关联（换班 → 指标变化）
- [ ] 西门子 Opcenter REST API 适配
- [ ] 鼎捷 MES API 适配
- [ ] MQTT Connector (订阅设备实时数据)
- [ ] OPC UA Connector (PLC 数据读取)
- [ ] 实时告警推送 (WebSocket)
- [ ] 根因分析报告生成 (Markdown + 图表)

### Success Criteria
- 良率异常能在5分钟内检测并告警
- 根因分析报告准确率 > 70%（人工验证）
- 支持至少3种主流MES系统

---

## Phase 3: Operations (Month 5-6)

**Goal: 生产就绪 + 智能排产**

### Deliverables
- [ ] Schedule Agent (智能排产)
- [ ] 边缘部署完整方案
- [ ] 权限管理 (RBAC)
- [ ] 审计日志系统
- [ ] 性能优化
- [ ] 生产环境部署文档

### Technical Tasks
- [ ] Schedule Agent: 约束满足问题求解
  - 产能约束
  - 人员技能约束
  - 物料可用性约束
  - 设备维护窗口约束
  - 交期优先级
- [ ] 排产可视化 (甘特图)
- [ ] 边缘节点管理
  - 模型下载/更新
  - 离线模式降级策略
  - 边缘-云同步
- [ ] RBAC: 管理员/工程师/操作员/只读
- [ ] 审计日志: 所有Agent操作可追溯
- [ ] 数据库优化: TimescaleDB 时序数据
- [ ] 连接池 + 缓存策略
- [ ] 压力测试: 100并发查询

### Success Criteria
- 排产建议考虑所有约束，方案可执行率 > 80%
- 边缘模式下核心功能可用（无外网）
- 100并发 < 3秒响应
- 审计日志完整覆盖所有操作

---

## Phase 4: Ecosystem (Month 7+)

**Goal: 平台化 + 生态建设**

### Deliverables
- [ ] 连接器插件市场
- [ ] 多工厂联邦架构
- [ ] 企业级功能 (SSO, 多租户)
- [ ] 自定义Agent开发SDK
- [ ] 行业解决方案包
- [ ] 社区建设

### Technical Tasks
- [ ] 连接器插件规范 + CLI工具
- [ ] 多工厂数据聚合层
- [ ] SAML/OIDC SSO
- [ ] 多租户数据隔离
- [ ] Agent开发SDK (Python/TypeScript)
- [ ] 行业包:
  - SMT行业包 (锡膏印刷、贴片、回流焊优化)
  - 组装行业包 (工位平衡、节拍优化)
  - 测试行业包 (测试覆盖率、假阳性分析)
- [ ] 集成测试框架
- [ ] CI/CD pipeline

---

## Long-term Vision

### Year 1
- 成为开源MES Agent中间件的事实标准
- 支持10+种MES系统
- 社区 1000+ stars
- 3-5个生产环境案例

### Year 2
- Agent Marketplace（第三方Agent）
- 数字孪生集成
- 跨工厂知识迁移
- 商业版（企业支持 + 托管服务）

### Year 3
- 工业AI Agent标准推动
- 垂直行业深度解决方案
- 国际化（英文/日文/韩文）
