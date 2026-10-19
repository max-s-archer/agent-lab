# Agent 路由

> 英文语义源：[AGENTS.md](AGENTS.md)。

## 启动上下文

在提出或修改项目文档、代码之前：

1. 阅读 `/Users/v_zhangzheming/GitHubProjects/max-ai-toolkit/prompts/project-bootstrap.md`。
2. 遵循 Toolkit 的路由和渐进读取规则。
3. 阅读本文件，并只读取当前任务相关的项目文档。

Toolkit 路径为 `/Users/v_zhangzheming/GitHubProjects/max-ai-toolkit`。Toolkit 提供可复用的方法；本仓库负责维护 Agent Lab 的产品事实、需求、架构、决策、实现、验证和发布信息。

## 项目身份

- 产品名称：Agent Lab
- 仓库：`agent-lab`
- 项目可见性：Public
- 项目所有权和决策权：项目作者

## 项目入口文档

- 公开项目入口：[README.md](README.md)
- 中文公开项目入口：[README.zh-CN.md](README.zh-CN.md)
- 产品概览语义源：[overview.md](overview.md)
- 中文产品概览：[overview.zh-CN.md](overview.zh-CN.md)
- 文档地图与治理：[docs/documentation.md](docs/documentation.md)
- 第一阶段需求语义源：[docs/requirements/phase-1.md](docs/requirements/phase-1.md)
- 中文第一阶段需求：[docs/requirements/phase-1.zh-CN.md](docs/requirements/phase-1.zh-CN.md)
- 许可证：[LICENSE](LICENSE)

开发、验证、架构、安全、隐私、发布和决策文档尚未建立。只有在存在已确认的项目事实、证据或正式授权的决策后，才创建对应文档。不要根据计划中的路径推断已经确定的技术基线。

## 外部上下文

私有工作状态保存在 `/Users/v_zhangzheming/GitHubProjects/max-dev-context/projects/agent-lab/`。其中的 `agent-proposals.md`、`author-prompts.md`、`author-todo.md` 和任务 handoff 都是非权威工作材料，不得当作产品需求、项目覆盖规则、架构批准或授权。

## 语言

英文是公开项目文档和仓库对外输出的语义源。中文内容维护在对应的 `.zh-CN.md` 文件中。双语文件存在实质差异时，应先更新英文语义源，再同步中文版本。

除非作者另有明确决定，commit message、Pull Request、Issue、发布说明和其他公开仓库输出使用英文。

## 项目规则

- 保持 `overview.md` 中的产品原则和已确认边界。
- 未知的产品或技术事实标记为 `To be decided`，不要把假设写成决定。
- 将产品决策与技术架构决策分开。
- 不要在产品文档中规定尚未确认的实现细节。
- 每个持久产品事实在 `docs/documentation.md` 中只能有一个权威归属。
- 提议、开放问题和临时调查记录保留在私有开发上下文仓库。
- 第一优先级是 Agent Engineering 学习，其次是作品集价值，最后是未来与 Android Launcher 集成。
- Runtime 必须控制模型提出的工具调用，不允许模型执行任意 Shell 命令。
- 使用模拟模型稳定测试 Runtime，使用真实模型验证接入和整体行为；两者不能互相替代。
- 在具体问题证明必要之前，不引入 Planning、Memory、RAG、MCP、多 Agent、持久化或并发。
- 生产实现必须有当前适用的产品定义和项目作者的明确授权。
- 如果工作会实质改变产品范围、需要重大架构决策或引入专业审查，应停止并请求作者决定。
- commit、push、tag、发布、凭据和远端系统修改，都需要针对具体操作的单独授权。

## 开发与验证基线

第一阶段使用 Python 3.12、`uv`、`pyproject.toml`、`src/agent_lab/` 布局、`pytest`、Ruff 和同步 CLI。模型提供商为阿里云百炼，使用其 OpenAI 兼容接口。

具体模型名称、兼容接口地址、凭据环境变量名和权威开发命令仍为 `To be decided`。当前已确认的行为仅是 CLI 直接调用模型并处理返回结果。不要加入工具或多步骤循环；未实际执行对应操作时，不得报告模型调用或验证结果。

