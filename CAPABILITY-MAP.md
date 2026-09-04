---
type: ssot
owner: governance-team
last_updated: 2026-09-03
---

# Model-Driven 能力地图

> 全生命周期模型驱动平台 · M2类型 (见 project-registry.yaml) · 阶段 (见 project-registry.yaml) · 工具 (见 project-registry.yaml)
>
> **数字纪律 (SSOT)**: 下方计数仅为 as_of 快照, 唯一真源是 `project-registry.yaml`
> + 代码 (`m2_lifecycle.py` / `stages.py` / `tools.py` / CI). 由
> `bin/mof/check-mof-capabilities-drift.py` 守护 (ADR-0238 P0-3).
> 不在文档复制数量 (model-driven CLAUDE.md 铁律). **as_of**: 2026-07-25

---

## 一、架构定位

```
┌─────────────────────────────────────────────────────────────┐
│                    Model-Driven — 模型驱动平台                 │
├─────────────────────────────────────────────────────────────┤
│  M2类型  │  阶段  │  工具  │  Pipeline  │  Derivation        │
│  (见 project-registry.yaml / 代码 SSOT — 计数不在此复制)        │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、核心功能

| 功能 | 说明 | 测试数 |
|------|------|--------|
| M2类型 | 元模型类型 (见 `m2_lifecycle.py` / project-registry.yaml) | 见 CI |
| 阶段 | 生命周期阶段管理 (见 `stages.py`) | 见 CI |
| 工具 | 模型操作工具 (见 `tools.py`) | 见 CI |
| Pipeline | 数据处理管线 (见 `pipeline.py`) | 见 CI |

---

## 三、CLI 命令

```bash
model-driven status     # 状态
model-driven pipeline   # 管线
model-driven derive     # 推导
```

---

## 四、测试覆盖

| 模块 | 测试用例 |
|------|----------|
| M2类型 / 阶段 / 工具 / 管线 | 以 `uv run pytest tests/ -q` 实际输出为准 (SSOT) |

> 测试总数/通过率以本项目 CI 为准, 不在此硬编码 (避免漂移).

---

*版本: 0.1.0 · 更新: 2026-07-25 (P0-3 数字指针化, ADR-0238)*
