# 项目命名与 GitHub 搜索建议

## 当前名字：ManuGent

`ManuGent` 来自：

```text
Manufacturing + Agent
```

优点：

- 有品牌感
- 简短
- 和制造业 Agent 方向相关

缺点：

- 不是常见搜索词
- 用户不一定能从名字立刻看出 MES
- GitHub 搜索流量不如关键词型仓库名

## 如果目标是 GitHub 搜索流量

仓库名最好包含直接关键词：

| 名称 | 搜索优势 | 品牌感 |
|------|----------|--------|
| `mes-agent` | 很强 | 一般 |
| `mes-ai-agent` | 很强 | 一般 |
| `manufacturing-agent` | 强 | 中等 |
| `factory-agent` | 中等 | 较好 |
| `industrial-ai-agent` | 强 | 中等 |
| `manugent` | 弱 | 较好 |

## 建议方案

推荐：

```text
GitHub 仓库名：mes-agent
项目品牌名：ManuGent
一句话描述：MES Agent reference architecture for manufacturing intelligence
```

这样做的好处：

- `mes-agent` 更容易被搜索到
- README 里仍然保留 ManuGent 品牌
- GitHub description 可以覆盖更多关键词

## 推荐 GitHub Description

```text
MES Agent reference architecture for manufacturing AI: tool calling, root-cause analysis, evidence chain, memory, audit, and approval workflow.
```

## 推荐 Topics

```text
mes
manufacturing
ai-agent
industrial-ai
factory
smart-manufacturing
root-cause-analysis
mcp
llm
agentic-ai
quality-management
traceability
oee
```

## 是否现在改名

可以改，但建议先确认：

1. 是否希望仓库 URL 从 `manugent` 变成 `mes-agent`
2. 是否已有外部链接引用旧 URL
3. 是否接受本地 remote URL 更新

如果改名，建议只改 GitHub 仓库名，不改 Python package 名：

```text
Repository: mes-agent
Package: manugent
Brand: ManuGent
```
