# Agent Lab

Agent Lab 是一个公开的 Python 工程实验室，用于学习和构建可靠的 LLM Agent 系统。

项目以 CLI 作为第一种交互入口，重点理解 Agent 背后的执行机制：模型调用、结构化工具请求、Runtime 控制、请求校验、失败处理、测试和运行轨迹。

## 当前状态

规划中

## 项目目标

项目有三个相互关联的目标，优先级如下：

1. 通过真实且持续演进的项目，建立 Agent Engineering 实践能力。
2. 沉淀一个清晰、可测试、可解释的公开 GitHub 作品集项目。
3. 为未来可能与 Launcher4Max 集成保留可复用的协议和工程经验。

## 第一阶段

第一阶段目标是建立初步的模型 API 调用能力，并实现一个最小的受控 Agent Loop：

```text
用户输入
  → Runtime
  → 模型决策
  → 工具请求校验
  → 工具执行
  → 工具结果返回模型
  → 最终回答或继续执行受控步骤
```

这一阶段用于建立对模型调用和 Runtime 控制机制的初步理解。详细需求见[第一阶段需求](docs/requirements/phase-1.zh-CN.md)。

## 范围边界

项目不会一开始就建设通用 Agent 平台。Planning、Memory、RAG、MCP、多 Agent 协作、持久化、并发、任意 Shell 执行和高风险系统修改暂不属于第一阶段，除非真实问题证明它们确有必要。

## 文档

- [项目概览](overview.zh-CN.md)
- [英文项目概览](overview.md)
- [文档地图](docs/documentation.md)
- [第一阶段需求](docs/requirements/phase-1.zh-CN.md)
- [英文第一阶段需求](docs/requirements/phase-1.md)
- [Agent 路由](AGENTS.zh-CN.md)

## 许可证

本项目使用 Apache License 2.0，详见 [LICENSE](LICENSE)。

