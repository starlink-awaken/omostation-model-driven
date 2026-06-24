# AGENTS.md — model-driven Development Guide

> eCOS v5 Cross-Cutting Framework · 全生命周期模型驱动平台

## Quick Commands

```bash
cd projects/model-driven
uv run pytest tests/ -q          # 190 tests, 100% pass
uv run ruff check src/           # Lint check
uv run ruff check --fix src/     # Auto-fix
uv run ruff format src/          # Format
uv run model-driven --help       # CLI help
```

## Architecture

model-driven 是 **Cross-Cutting Framework (横切面框架)**，不归属任何单一层。被 L0/I0/L3/L4 消费，自身零内部依赖。

### 消费关系

```
L4 l4-kernel ──→ model-driven (lifecycle, omo_bridge)
L3 cockpit   ──→ model-driven (MCP tools, CLI bridge)
I0 agora     ──→ model-driven (28 MCP tools)
L0 ecos      ──→ model-driven (M1 nodes, 自反验证)
```

### 模块职责

| 模块 | 职责 | 文件数 |
|------|------|:--:|
| lifecycle/ | 7阶段引擎 + 门禁 + 流水线 + 追踪 | 5 |
| management/ | Spec/ADR/OKR 管理 + OMO 桥接 + Agent 协作 | 5 |
| mof/ | M3/M2 元模型扩展 + 本体论 | 3 |
| toolchain/ | 12工具 + 推导引擎 + Trigger + 扫描/建模/提炼 | 9 |
| ssot/ | 生命周期/价值 SSOT + 跨阶段检查 | 1 |
| 入口 | CLI (7子命令) + MCP Server (28 tools) | 2 |

## Key Dependencies

- **pyyaml>=6.0** — 唯一外部依赖
- 零 eCOS 项目依赖

## Testing Pattern

```bash
cd projects/model-driven
uv run pytest tests/ -q                    # 全量
uv run pytest tests/ -k "keyword" -q       # 按关键字
uv run pytest tests/test_tools.py -q       # 单个文件
```

## File Organization

- `src/model_driven/` — 27 个源文件 (5子包 + 3入口文件)
- `tests/` — 11 个测试文件, 190 tests

## Workspace-Wide Governance (2026-06-24)

This project follows the workspace-level governance conventions documented in the root `AGENTS.md`:

- **Agent Mutation Protocol**: Any autonomous agent/cron/daemon that modifies workspace state must emit `agent_mutation_intent`, avoid direct file I/O to `.omo/`/`spaces/`, and commit immediately. See `.omo/standards/agent-mutation-protocol.md` for the full protocol.
- **SSOT Guardian**: Run `python3 bin/ssot-guardian.py` from the workspace root before committing to detect task-count, current-wave, submodule-pointer, or direct-omo-io drift.
- **direct-omo-io**: Scripts must route writes to `.omo/` through `omo CLI`, `projects/omo` core, or `projects/c2g` ingress — never via raw `open()/mkdir()/write_text()`.
- **Submodule Governance**: Commit changes inside the submodule first, then bump the root-repo pointer; `git submodule status` with a `+` prefix indicates pending drift.
