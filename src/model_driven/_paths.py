"""model-driven 公共路径工具

提供统一的 workspace 和 state 目录获取，替代各处硬编码的 ~/Workspace 路径。
"""

import os
import warnings
from pathlib import Path


def get_workspace_dir() -> Path:
    """获取 eCOS workspace 根目录。

    优先使用 ECOS_WORKSPACE 环境变量，fallback 到 ~/Workspace。
    当环境变量未设置时发出 UserWarning，提醒显式配置。
    """
    env_path = os.environ.get("ECOS_WORKSPACE")
    if env_path:
        ws = Path(env_path)
        if not ws.exists():
            warnings.warn(f"ECOS_WORKSPACE 指向的路径不存在: {ws}", stacklevel=2)
        return ws

    # fallback: 相对脚本找 omostation workspace 根 (不硬编码 ~/Workspace, CI 可移植).
    # _paths.py 在 projects/model-driven/src/model_driven/, parents[4] = omostation 根.
    return Path(__file__).resolve().parents[4]


def get_state_dir() -> Path:
    """获取 model-driven 状态目录。

    返回 <workspace>/.omo/state/model-driven/。

    目录创建属于治理写操作，必须由调用方通过 OMO broker / helper 显式完成，
    这里不再隐式落盘。
    """
    return get_workspace_dir() / ".omo" / "state" / "model-driven"
