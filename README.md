# amax — AirymaxCompute

One command to install, run, and supervise local LLM inference — on x86_64, aarch64, and riscv64.

```bash
amax pull qwen3:8b
amax run qwen3:8b
```

> 中文版：[README_zh.md](README_zh.md)

## What it is

`amax` is an integration and supervision layer on top of proven open-source
inference components. It does not re-implement the engine, the operators, or
the compiler — it packages them, routes between hardware backends, keeps
long-running agent tasks alive, and makes the result machine-verifiable.

| Layer | Role | Source |
|---|---|---|
| Engine / operators | Tensor compute, GGUF inference, built-in OpenAI & Anthropic compatible API | [llama.cpp / ggml](https://github.com/ggml-org/llama.cpp) (MIT) |
| `amax` | Install, backend detection & routing, model fetching, process supervision, task-level evaluation | this project (Apache-2.0) |
| Agent runtime | Long-task checkpointing, crash self-healing, tool/inference isolation | [AirymaxRT](https://github.com/openairymax/agentrt) (optional) |
| OS | Large-page residency, inference QoS scheduling, DMA passthrough, acceptance tests | [AirymaxOS](https://github.com/openairymax) (optional) |

The stack is intentionally detachable: `amax` runs standalone on any Linux
macOS or Windows host (L0/L1 capability), and unlocks supervision and QoS
capabilities (L2/L3) when the full Airymax stack is present.

## Design principles

- **No vendor lock-in.** Hardware differences are isolated in dynamically
  loaded backend plugins; no chip vendor receives exclusive treatment.
- **Three architectures, no second-class citizens.** x86_64 for reach,
  riscv64 for first-class support where mainstream runtimes lack it,
  aarch64 because upstream already makes it nearly free.
- **Upstream first.** Fixes go upstream (llama.cpp, RISE) before they land here.
- **Core stays open.** Apache-2.0 core, permanently. Enterprise features ship
  as separate plugins and never reduce the open core.

## Status

Project bootstrap. The first alpha (`amax` v0.1, x86_64 + aarch64) is in
development. Design documentation will be published under `docs/` as it lands.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Third-party components retain their own licenses: llama.cpp / ggml (MIT),
OpenBLAS (BSD), PyTorch riscv64 wheels (BSD). No AGPL components are used in
the core.
