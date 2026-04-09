#!/usr/bin/env python
import subprocess
import sys
from pathlib import Path
import os   # <--- 添加这一行

# 切换到项目根目录
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)

# 创建必要目录
for d in ['data/processed', 'outputs/figures', 'outputs/tables', 'reports']:
    (PROJECT_ROOT / d).mkdir(parents=True, exist_ok=True)

print("=== Step 1: Load and clean data ===")
subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "load_data.py")])

print("\\n=== Step 2: Quality check ===")
subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "quality_check.py")])

print("\\n=== Step 3: Co-citation network ===")
subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "networks" / "co_citation.py")])

print("\\n=== Step 4: Collaboration network ===")
subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "networks" / "collaboration.py")])

print("\\n=== All steps completed. Check outputs/ and reports/ ===")