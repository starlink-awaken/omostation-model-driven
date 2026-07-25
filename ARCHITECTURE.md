# model-driven — Architecture

> **Layer**: M0 横切框架  
> **Role**: 模型驱动生命周期引擎 — M3→M2→M1 桥接  
> **Stack**: Python, uv, pytest, ruff; zero internal eCOS deps  
> **Health**: See local CI and model validation
> **SSOT**: 运行时健康、测试通过率、工具链规模以本项目 CI、模型校验和 workspace governance SSOT 为准
> **数字纪律**: 阶段/工具/规则计数以代码为 SSOT (`stages.py`/`tools.py`/`derivation_engine.py`), 不在文档复制数量 (model-driven CLAUDE.md 铁律). as_of: 2026-07-25
>
> 系统全景参见：[`../../docs/PANORAMA.md`](../../docs/PANORAMA.md)

---

## 1. 内部架构

```mermaid

graph TB
    M3[M3 Standards] --> M2[M2 Schemas]
    M2 --> M1[M1 Instances]
    DE[Derivation Engine] --> M2
    Tools[Tools: 见 tools.py] --> DE
    MCP[MCP Server] --> Tools

```

## 2. 入口

| Type | Entry | Port / Notes |
|:--|:--|:--|
| CLI | `model-driven` | status/pipeline/derive/... |
| MCP stdio | `src/model_driven/mcp_server.py` | MCP tools (以 `_register_tool` 实际计数为准, ADR-0238 P0-4) / managers (以实际为准) |

## 3. 核心模块

| Module | Responsibility |
|:--|:--|
| `src/model_driven/lifecycle/stages.py` | lifecycle stages + state machine (计数见代码) |
| `src/model_driven/toolchain/tools.py` | core model-driven tools (计数见代码) |
| `src/model_driven/toolchain/derivation_engine.py` | DR rules + triggers (计数见代码) |
| `src/model_driven/mcp_server.py` | MCP server |
| `src/model_driven/cli.py` | CLI entry |

## 4. 测试

```bash
cd projects/model-driven && uv run pytest tests/ -q
```

## 架构概览

参见工作区架构概览图：[`../../docs/ARCHITECTURE-DIAGRAM.md`](../../docs/ARCHITECTURE-DIAGRAM.md)
