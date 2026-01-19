#!/usr/bin/env bash

set -euo pipefail

# 切换到脚本所在目录（防止被 cron / workflow 从别处调用）
cd "$(dirname "$0")"

echo "========== $(date '+%Y-%m-%d %H:%M:%S') =========="

# 运行 Python 脚本
python3 gen_m3u.py

# 如果 tv.m3u 没有变化，则直接退出
if git diff --quiet -- tv.m3u; then
    echo "No changes in tv.m3u. Nothing to commit."
    exit 0
fi

# 提交并推送
git add tv.m3u
git commit -m "Auto update tv.m3u"
git push

