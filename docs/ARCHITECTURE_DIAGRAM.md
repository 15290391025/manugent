# ManuGent 架构介绍图

这张图用于在 README、作品集或技术介绍中快速说明 ManuGent 的整体架构。

```mermaid
flowchart TB
    user["用户<br/>工程 / 班长 / 质量 / 设备"]
    demo["Web Demo / CLI / API"]
    api["FastAPI Gateway<br/>/chat /query /workflows"]

    session["Session Manager<br/>会话隔离 + memory scope"]
    agent["MES Agent Core<br/>LLM + 受控工具调用"]
    rca_workflow["LangGraph RCA Workflow<br/>生产 → 质量 → 设备 → 证据 → 报告"]

    tools["Manufacturing Tool Protocol<br/>typed MES tools + safety levels"]
    memory["Memory Store<br/>session / incident / factory fact / preference / audit"]
    evidence["Evidence Chain<br/>production / quality / material / equipment / memory"]

    demo_connector["DemoMESConnector<br/>作品集演示数据"]
    rest_connector["RestConnector<br/>真实 MES API 适配"]

    mes["MES"]
    qms["QMS"]
    erp["ERP"]
    equipment["设备 / IoT / PLC"]
    approval["企业审批边界<br/>MES / BPM / Lark / 自研流程"]

    user --> demo --> api
    api --> session --> agent
    agent --> rca_workflow
    agent --> tools
    rca_workflow --> tools
    rca_workflow --> evidence
    session <--> memory
    agent --> memory
    rca_workflow --> memory
    tools --> demo_connector
    tools --> rest_connector
    rest_connector --> mes
    rest_connector --> qms
    rest_connector --> erp
    rest_connector --> equipment
    evidence --> api
    tools -. action tools .-> approval

    classDef entry fill:#eef6ff,stroke:#2563eb,color:#172554
    classDef agentLayer fill:#f0fdf4,stroke:#16a34a,color:#052e16
    classDef dataLayer fill:#fff7ed,stroke:#f97316,color:#431407
    classDef systemLayer fill:#f8fafc,stroke:#64748b,color:#0f172a
    classDef boundary fill:#fef2f2,stroke:#dc2626,color:#450a0a

    class user,demo,api entry
    class session,agent,rca_workflow,tools agentLayer
    class memory,evidence dataLayer
    class demo_connector,rest_connector,mes,qms,erp,equipment systemLayer
    class approval boundary
```

## 如何讲解这张图

ManuGent 位于“人”和“工厂系统”之间。用户通过 Web、CLI 或 API 发起问题，
API 创建隔离会话，然后由 MES Agent 通过受控工具调用回答问题，或者进入
LangGraph 根因分析 workflow。

Agent 不直接访问任意数据库，而是通过 Manufacturing Tool Protocol 调用
typed MES tools。工具协议定义了参数、返回结构、安全级别和连接器边界，
这样更容易审计，也更适合接入已有 MES、QMS、ERP 和设备系统。

Memory 是架构中的一等能力。会话历史、历史异常、工厂事实、用户偏好和
审计事件被拆开管理，避免不同用户、不同工厂、不同场景的上下文混在一起。

审批被画成外部边界是刻意设计。ManuGent 可以识别哪些 action tool 跨过
安全边界，但真正的审批路由、超时、升级、代办、执行权限，通常属于 MES、
BPM、Lark/飞书或企业自研流程平台。

## RCA LangGraph 细节

```mermaid
flowchart LR
    question["良率下降问题"]
    production["query_production"]
    quality["query_quality"]
    equipment["query_equipment"]
    evidence["build_evidence"]
    report["build_report"]

    question --> production --> quality --> equipment --> evidence --> report
```

当前实现的 LangGraph workflow 是线性的。这不是缺点，而是为了先把制造业分析
路径显式化：先查生产，再查质量，再查设备，然后构造证据链并生成报告。
后续可以继续扩展成条件路由、失败重试、多 Agent supervisor 等模式。
