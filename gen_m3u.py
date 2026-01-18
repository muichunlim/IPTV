import requests
import re
from collections import OrderedDict

INPUT_URL = "https://live.catvod.com/tv.m3u"
OUTPUT_FILE = "tv.m3u"

GROUP_ORDER = [
    "港澳频道",
    "马来西亚",
    "新加坡",
    "Singapore",
    "台湾",
    "香港",
    "中国",
    "新闻频道",
    "电影频道",
    "纪录频道",
    "体育频道",
    "儿童频道",
]

# 仅用于「马来西亚」的 tvg-name 关键词
MY_TVG_KEYWORDS = [
    "8TV",
    "AEC",
    "AOD",
    "华丽台",
    "欢喜台",
    "Astro QJ",
    "爱奇艺",
    "星河台",
    "TVB",
    "Celestial",
]

# 仅用于「Singapore / 新加坡」的 tvg-name 关键词
SG_TVG_KEYWORDS = [
    "Channel",
    "CNA",
]

group_entries = OrderedDict((g, []) for g in GROUP_ORDER)

resp = requests.get(INPUT_URL, timeout=15)
resp.raise_for_status()

# Save original m3u
with open("origin_tv.m3u", "wb") as f:
    f.write(resp.content)
lines = resp.text.splitlines()

i = 0
while i < len(lines) - 1:
    line = lines[i].strip()
    if not line.startswith("#EXTINF"):
        i += 1
        continue

    url = lines[i + 1].strip()

    # 提取 group-title
    group_match = re.search(r'group-title="([^"]+)"', line)
    if not group_match:
        i += 2
        continue

    group = group_match.group(1)
    if group not in group_entries:
        i += 2
        continue

    # 如果是「马来西亚」，额外检查 tvg-name
    if group == "马来西亚":
        tvg_match = re.search(r'tvg-name="([^"]*)"', line)
        tvg_name = tvg_match.group(1) if tvg_match else ""

        if not any(k.lower() in tvg_name.lower() for k in MY_TVG_KEYWORDS):
            i += 2
            continue

    # 如果是「Singapore / 新加坡」，额外检查 tvg-name
    if group in ["Singapore", "新加坡"]:
        tvg_match = re.search(r'tvg-name="([^"]*)"', line)
        tvg_name = tvg_match.group(1) if tvg_match else ""

        if not any(k.lower() in tvg_name.lower() for k in SG_TVG_KEYWORDS):
            i += 2
            continue

    group_entries[group].append(f"{line}\n{url}\n")
    i += 2

# 输出新的 m3u
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="http://epg.catvod.com/epg.xml"\n')
    for group in GROUP_ORDER:
        for entry in group_entries[group]:
            f.write(entry)

print(f"Done. Output file: {OUTPUT_FILE}")
