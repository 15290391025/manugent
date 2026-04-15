# 推广文章

---

## 标题选项

1. 「开源」ManuGent - 给工厂MES系统装上AI大脑，用自然语言对话你的产线
2. 我做了一个开源项目，让工厂工程师用说人话的方式操作MES
3. 别再用Excel分析产线数据了——这个开源AI Agent让你直接问MES

---

## 掘金/V2EX/CSDN 发帖内容

### 正文

做了个开源项目，解决一个很痛的问题：

**在工厂里查个数据太麻烦了。**

想象一个场景：品质工程师发现良率下降了，他需要：
1. 打开MES系统 → 筛选产线 → 选日期 → 导出报表
2. 打开Excel → 做数据透视 → 画趋势图
3. 再去设备系统查告警记录
4. 再去物料系统查批次变更
5. 最后综合分析，写报告，汇报

**这一套下来，半天就没了。**

如果有个AI Agent，直接问一句话：

```
"3号线最近3天贴片良率从99.2%掉到了97.1%，帮我分析原因"
```

然后Agent自动：
- 从MES拉良率数据
- 关联设备告警记录
- 匹配物料切换时间线
- 分析出根因：锡膏印刷偏移 + 新批次物料公差偏大
- 给出建议措施

**这就是 ManuGent 要做的事。**

### 项目定位

ManuGent 不是替代你现有的MES，而是在MES上面加一层AI Agent中间件。

```
[你现有的MES] <--对接--> [ManuGent AI层] <--提供--> [自然语言交互]
```

不管你是用西门子Opcenter、鼎捷、摩尔元数还是自研MES，都可以对接。

### 技术栈

- **Agent框架**: LangGraph (有状态多步推理)
- **协议**: MCP Manufacturing Extension (标准化Agent↔MES通信)
- **后端**: FastAPI (异步高性能)
- **LLM**: 支持 OpenAI / Claude / Qwen / 本地Ollama
- **工业协议**: OPC UA / MQTT (对接设备层)
- **边缘部署**: 支持本地推理，工厂不连外网也能用

### 和现有方案的区别

| 维度 | ManuGent | 西门子+AI | 鼎捷+AI |
|------|----------|----------|---------|
| 开源 | ✅ MIT | ❌ | ❌ |
| 绑定MES | 不绑定，任意MES | 绑定Opcenter | 绑定鼎捷 |
| 价格 | 免费 | 百万级 | 百万级 |
| 边缘部署 | ✅ Ollama | ❌ | ❌ |
| 中文原生 | ✅ | ❌ | ✅ |

### 现在的状态

项目刚起步，完成了基础架构：
- MCP制造协议（10个工具定义）
- REST MES连接器
- 自然语言查询Agent
- FastAPI服务器
- CLI工具

**最缺的是什么？**
- 有MES行业经验的伙伴（帮我验证需求）
- 在真实工厂环境测试
- 更多MES系统的连接器

### 链接

GitHub: https://github.com/15290391025/manugent

欢迎star、fork、提issue，特别是如果你在工厂干过，告诉我你的MES有多难用 😂

---

## 知乎回答模板

**问题：MES系统有哪些痛点？/ 工厂数字化转型难在哪里？/ AI在制造业能做什么？**

回答：

在工厂干过的都知道，MES系统最大的问题不是功能不够，而是**太难用了**。

查个数据要开5个系统，导Excel分析半天，写报告又半天。良率下降了排查根因要翻遍设备日志、物料记录、人员排班...

这就是为什么我觉得"AI Agent + MES"会是一个大方向。

最近发现一个开源项目 ManuGent，做的事情很有意思：
- 不是替代MES，而是给MES加一个AI大脑
- 用自然语言直接问产线数据
- 自动关联分析异常原因
- 支持边缘部署（工厂不连外网也能用）

虽然是早期项目，但方向我觉得对。

GitHub: https://github.com/15290391025/manugent

---

## Twitter/X 发帖

```
🧠 Just open-sourced ManuGent - AI Agent middleware for Manufacturing Execution Systems.

Give your factory MES a brain. Ask questions like:
"Line 3 yield dropped from 99.2% to 97.1%, why?"

Agent auto-analyzes: equipment logs + material changes + process data → root cause.

✅ Works with ANY MES (Siemens, SAP, custom)
✅ MCP protocol for standardized agent-MES comms
✅ Edge deployment (Ollama for offline factories)
✅ MIT license

https://github.com/15290391025/manugent

#Manufacturing #AIagent #MES #Industry40 #OpenSource
```

---

## Reddit 发帖

**r/manufacturing, r/PLC, r/automation, r/opensource**

```
Title: Open-sourcing an AI Agent for Manufacturing Execution Systems

I've been working on ManuGent - an open-source AI agent middleware that connects to existing MES systems and provides natural language interaction.

Instead of navigating through 5 different screens to check OEE, you just ask:
"What's Line 3's OEE today?"

Or when quality drops:
"Why did yield drop from 99.2% to 97.1% over the last 3 days?"

The agent automatically pulls data from MES, correlates with equipment alarms, material changes, and personnel shifts to find the root cause.

Key features:
- Non-invasive: sits on top of your existing MES, doesn't replace it
- MCP-based protocol for standardized agent-MES communication
- Supports any MES with REST API (Siemens, SAP, custom)
- Edge deployment with Ollama for offline factory environments
- MIT licensed

Early stage, looking for feedback from people who've worked on factory floors.

GitHub: https://github.com/15290391025/manugent
```
