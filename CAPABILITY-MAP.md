# Model-Driven 能力地图

> 全生命周期模型驱动平台 · M2类型 (见 project-registry.yaml) · 阶段 (见 project-registry.yaml) · 工具 (见 project-registry.yaml)

---

## 一、架构定位

```
┌─────────────────────────────────────────────────────────────┐
│                    Model-Driven — 模型驱动平台                 │
├─────────────────────────────────────────────────────────────┤
│  M2类型 (见 project-registry.yaml)  │  阶段 (见 project-registry.yaml)  │  工具 (见 project-registry.yaml)  │  Pipeline  │  Derivation │
│  24 Types│  7 Phase │  12 Tools│  Pipeline │  Derivation  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、核心功能

| 功能 | 说明 | 测试数 |
|------|------|--------|
| M2类型 (见 project-registry.yaml) | 24 个元模型类型 | 8 |
| 阶段 (见 project-registry.yaml) | 生命周期阶段管理 | 8 |
| 工具 (见 project-registry.yaml) | 模型操作工具 | 8 |
| Pipeline | 数据处理管线 | 4 |

---

## 三、CLI 命令

```bash
model-driven status     # 状态
model-driven pipeline   # 管线
model-driven derive     # 推导
```

---

## 四、测试覆盖

| 模块 | 测试文件 | 测试用例 |
|------|----------|----------|
| M2类型 (见 project-registry.yaml) | 8 | ~60 |
| 阶段 | 8 | ~60 |
| 工具 | 8 | ~60 |
| 管线 | 4 | ~30 |
| **总计** | **28** | **~210** |

---

*版本: 0.1.0 · 更新: 2026-06-12*
