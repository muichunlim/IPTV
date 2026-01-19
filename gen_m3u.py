import requests
import re
from collections import OrderedDict

INPUT_URL = "https://live.catvod.com/tv.m3u"
OUTPUT_FILE = "tv.m3u"

GROUP_ORDER = [
    "港澳",
    "马来西亚",
    "新加坡",
    "Singapore",
    "其它",
    "台湾",
    "香港",
    "中国",
    "央视",
    "卫视",
    "新闻",
    "电影",
    "纪录",
    "记录",
    "体育",
    "儿童",
]

# 仅用于「马来西亚」的 tvg-name 关键词
MY_TVG_KEYWORDS = [
    "8TV",
    "TV8",
    "AEC",
    "AOD",
    "华丽台",
    "欢喜台",
    "全佳",
    "爱奇艺",
    "星河台",
    "TVB",
    "Celestial",
]

# 仅用于「Singapore / 新加坡」的 tvg-name 关键词
SG_TVG_KEYWORDS = [
    "Channel5",
    "Channel8",
    "ChannelU",
    "CNA",
    "MeWatch C",
]

group_entries = OrderedDict((g, []) for g in GROUP_ORDER)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://live.catvod.com/",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

session = requests.Session()
session.headers.update(HEADERS)

resp = session.get(INPUT_URL, timeout=20)
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
    group_match = re.search(r'group-title="([^"]*)"', line)
    if not group_match:
        i += 2
        continue

    group = group_match.group(1)

    matched_group = None
    for g in GROUP_ORDER:
        if g in group:
            matched_group = g
            break
            
    if not matched_group:
        i += 2
        continue

    # 如果是「马来西亚」，额外检查 channel_name
    if matched_group == "马来西亚":
        channel_name = line.rsplit(',', 1)[-1].strip()

        if not any(k.lower() in channel_name.lower() for k in MY_TVG_KEYWORDS):
            i += 2
            continue

    # 如果是「Singapore / 新加坡」，额外检查 channel_name
    if matched_group in ["Singapore", "新加坡"]:
        channel_name = line.rsplit(',', 1)[-1].strip()

        if not any(k.lower() in channel_name.lower() for k in SG_TVG_KEYWORDS):
            i += 2
            continue

    # 如果 matched_group 包含 "其它"，使用 MY 和 SG 关键词过滤
    if "其它" in matched_group:
        # 提取逗号后面的频道名称
        channel_name = line.rsplit(',', 1)[-1].strip()
        
        all_keywords = MY_TVG_KEYWORDS + SG_TVG_KEYWORDS
        if not any(k.lower() in channel_name.lower() for k in all_keywords):
            i += 2
            continue

    group_entries[matched_group].append(f"{line}\n{url}\n")
    i += 2

# 输出新的 m3u
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="http://epg.catvod.com/epg.xml"\n')
    for group in GROUP_ORDER:
        f.write("\n\n")
        for entry in group_entries[group]:
            f.write(entry)

print(f"Done. Output file: {OUTPUT_FILE}")
