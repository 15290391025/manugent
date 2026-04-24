# 项目故事：为什么需要 MES Agent

## 背景

MES 是工厂生产执行的核心系统，但很多 MES 在实际使用中仍然像一个复杂的表单和报表系统。

工程师要回答一个看似简单的问题：

```text
SMT-03 最近 24 小时良率为什么下降？
```

通常需要跨多个页面和系统：

- 生产 KPI
- 工单进度
- WIP
- 质量缺陷
- 设备告警
- 物料批次
- SN 追溯
- 历史异常报告

这不是单纯的“查询”问题，而是一个制造业场景下的数据关联和判断问题。

## ManuGent 的核心观点

ManuGent 的设计不是让 LLM 直接连接数据库，也不是让它绕过 MES 做决策。

它的核心观点是：

> Agent 应该站在 MES 之上，通过受控工具、证据链、记忆和审批边界，帮助人更快理解现场，而不是替代 MES 或替代人。

## 为什么不能让 Agent 直接查数据库

在工业场景里，让 LLM 直接查数据库有明显风险：

- 它可能查询错误表或错误字段
- 它可能绕过 MES 自身权限
- 它可能误解生产语义
- 它可能生成不可审计的结论
- 它可能在没有审批的情况下触发危险操作

所以 ManuGent 使用 **Manufacturing Tool Protocol**：

```text
LLM / Agent
  → typed MES tools
  → connector
  → MES / ERP / QMS
```

工具是可控的、可审计的、可分级的。

## 为什么证据链重要

制造业问题不能只给一个“可能是设备问题”的回答。

一个合格的 MES Agent 应该说明：

```text
生产证据：良率从 98.1% 下降到 92.4%
质量证据：主要缺陷是 solder_bridge
物料证据：缺陷集中在 SP-20260424-A 批次
设备证据：MOUNTER-03A 出现 nozzle pickup 告警
历史记忆：上次类似问题通过清洁 nozzle bank 解决
```

这就是 Evidence Chain。

## 为什么 memory 重要

工厂问题经常复发。优秀工程师的价值不仅是会查数据，还在于记得：

- 上次类似异常是什么原因
- 哪个物料批次容易出问题
- 哪条线的设备有历史隐患
- 哪位主管喜欢什么日报格式
- 哪些操作必须走审批

ManuGent 把这些经验拆成几类记忆：

- session memory
- episodic incident memory
- semantic factory memory
- preference memory
- audit memory

这参考了 ChatGPT 式记忆逻辑，但映射到了 MES 场景。

## 为什么审批和审计是底线

工业 Agent 和普通聊天机器人最大的不同是：它可能影响真实生产。

因此 ManuGent 的安全原则是：

- read-only 工具可以自动执行
- advisory 工具只给建议
- approval 工具必须人工确认
- restricted 工具默认禁止或只允许管理员
- 所有工具调用都进入 audit memory

## 这个项目展示什么能力

ManuGent 展示的是：

- 对 MES 核心对象的理解
- 对 Agent tool-calling 架构的理解
- 对制造业根因分析链路的理解
- 对 memory / audit / approval 的工程化理解
- 对企业安全边界的现实判断

它不是一个完整商业 MES，也不是一个简单聊天机器人。

它是一个 MES Agent 参考架构。
