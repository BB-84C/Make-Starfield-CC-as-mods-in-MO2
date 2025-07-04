import os
import shutil
import sys
import re
from pathlib import Path
from collections import defaultdict

# 获取 MO2Root 路径
if len(sys.argv) < 2:
    print("请提供 MO2Root 路径作为第一个参数。")
    sys.exit(1)

MO2_ROOT = Path(sys.argv[1])
SOURCE_FOLDER = MO2_ROOT / "overwrite"
TARGET_FOLDER = MO2_ROOT / "mods"
TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
# TARGET_FOLDER = MO2_ROOT / "bb84_plugins/test_mods"

# 创建目标目录
TARGET_FOLDER.mkdir(parents=True, exist_ok=True)

# 文件按前缀分类
file_groups = defaultdict(list)

def extract_prefix(filename: str) -> str | None:
    # 移除扩展名
    base = filename.rsplit('.', 1)[0]

    # 匹配以 `xxx - xxx` 或 `xxx.esm` 形式的前缀
    esm_match = re.match(r"(.+)\.esm$", filename, re.IGNORECASE)
    dash_match = re.match(r"(.+?) - .+\.(ba2|txt|xml|json|ini|.*)$", filename, re.IGNORECASE)

    if esm_match:
        return esm_match.group(1)
    elif dash_match:
        return dash_match.group(1)
    else:
        return None

for file in SOURCE_FOLDER.iterdir():
    if file.is_file() and not file.name.endswith(".mohidden"):
        prefix = extract_prefix(file.name)
        if prefix:
            file_groups[prefix].append(file)

# 复制文件并重命名原文件
for prefix, files in file_groups.items():
    dest_dir = TARGET_FOLDER / f"{prefix}-cc"
    dest_dir.mkdir(exist_ok=True)

    for file in files:
        shutil.copy(file, dest_dir / file.name)
        # file.rename(file.with_suffix(file.suffix + ".mohidden"))

print(f"处理完成：{len(file_groups)} 个 mod 文件夹已创建。")
