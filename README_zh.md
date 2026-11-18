# amax — 极境算力栈（AirymaxCompute）

一条命令完成本地 LLM 推理的安装、运行与看护——覆盖 x86_64、aarch64、riscv64 三种架构。

```bash
amax job submit job.yaml
amax receipt verify receipt.json
```

> 英文版：[README.md](README.md)

## 是什么

`amax` 是构建在成熟开源推理组件之上的**整合与看护层**。不自研推理引擎、不自建算子库、不重造编译器——它负责打包分发、硬件后端检测与路由、模型拉取、进程看护、长任务保活，并让结果可被机器验收。

| 层 | 职责 | 来源 |
|---|---|---|
| 引擎 / 算子 | 张量计算、GGUF 推理、内置 OpenAI 与 Anthropic 兼容 API | [llama.cpp / ggml](https://github.com/ggml-org/llama.cpp)（MIT） |
| `amax` | 安装、后端检测与路由、模型获取、进程看护、任务级评测 | 本项目（Apache-2.0） |
| Agent 运行时 | 长任务断点续传、崩溃自愈、工具/推理进程隔离 | [AirymaxRT](https://github.com/openairymax/agentrt)（可选） |
| 操作系统 | 大页驻留、推理 QoS 调度、DMA 直通、验收测试 | [AirymaxOS](https://github.com/openairymax)（可选） |

## 能力分级（L0–L3）

对每一款硬件，amax 给出可判定、可验证的承诺，而不是模糊的「已适配」：

| 级别 | 承诺 | 依赖 |
|---|---|---|
| **L0 跑得起来** | 纯 CPU 推理开箱即用 | 零厂商依赖 |
| **L1 接得上加速** | GPU/NPU 后端插件可用 | 看厂商开源程度 |
| **L2 管得住** | 进程隔离、QoS、资源配额 | 看协议，需 AirymaxRT / AirymaxOS |
| **L3 验得准** | 任务级评测由 CI 机器判定通过 | 完整栈 + 验收 harness |

口径：**L0 人人有，L1 看开源，L2/L3 看协议。**

## 可断开设计

`amax` 在任意 Linux / macOS / Windows 主机上独立运行（L0/L1）；接入 AirymaxRT 获得断点续传与崩溃自愈；部署 AirymaxOS 解锁 L2/L3 看护与验收能力。三层各自独立发布，任何一层缺席都不影响其余部分工作。amax 永不直接调用内核 syscall——与运行时的交互全部走 AirymaxRT 的字节级一致契约头。

## 设计原则

- **不绑定单一厂商。** 硬件差异隔离在动态加载的后端插件中（ggml `GGML_BACKEND_DL`）；没有任何芯片厂商获得排他待遇。
- **三架构，无二等公民。** x86_64 负责覆盖面，riscv64 提供主流运行时缺席的一等支持，aarch64 因上游完善而近乎免费。
- **上游优先。** 修复先回馈上游（llama.cpp、RISE），再落地本仓。
- **核心永久开源。** Apache-2.0 核心不缩水；企业功能以独立插件形式交付。

## 命名

- 命令与品牌名 `amax`，取自 Airy**max**——「极境」的「极」即 maximum。
- 仓库名 `compute`，与 agentrt 仓并列。
- 公开设计文档（ADR、后端插件接口规范、L0–L3 验收判据、评测方法论、芯片厂商接入指南）见 [openairymax/docs-compute](https://atomgit.com/openairymax/docs-compute)。

## 状态

项目引导期。首个 alpha（`amax` v0.1，x86_64 + aarch64）在研；设计文档随定稿逐步发布。

## 许可

Apache License 2.0，见 [LICENSE](LICENSE)。

第三方组件保留各自许可：llama.cpp / ggml（MIT）、OpenBLAS（BSD）、PyTorch riscv64 wheel（BSD）。核心不使用任何 AGPL 组件。
