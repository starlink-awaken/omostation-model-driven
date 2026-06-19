# model-driven — System Boundary

> 本文档描述 model-driven 与 eCOS 系统其他部分的边界：暴露的接口、依赖的上游、影响的下游。
>
> 架构演进对比参见：[`docs/ARCHITECTURE-EVOLUTION.md`](../docs/ARCHITECTURE-EVOLUTION.md)

---

## 1. 暴露接口

### BOS URI

model-driven 不直接注册 BOS URI 端点。它作为横切面框架被其他项目通过 Python import 消费，不走 BOS 路由。

### 入口

- **CLI**: `model-driven` status/pipeline/derive/...
- **MCP stdio**: `src/model_driven/mcp_server.py` 28 tools / 8 managers

## 2. 上游依赖

| 依赖 | 用途 | 类型 |
|------|------|------|
| pyyaml>=6.0 | YAML 解析 (M1/M2/M3 文件) | 运行时 |



## 3. 下游影响

- ecos (L0 MOF)
- agora (I0)
- cockpit (L3)
- l4-kernel (L4)

## 4. 配置 / SSOT

- 项目源码：`projects/model-driven/`
- 入口定义：`projects/model-driven/pyproject.toml` 或 `package.json`
- 测试：`cd projects/model-driven && uv run pytest tests/ -q`
