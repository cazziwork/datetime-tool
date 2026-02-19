"""
内閣府の祝日CSVを取得・キャッシュするユーティリティ。
CSV URL: https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
エンコーディング: Shift-JIS
キャッシュ有効期間: 1日
"""

import csv
import io
import os
import time
from datetime import date, datetime
from typing import Optional

import requests

HOLIDAY_CSV_URL = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
CACHE_FILE = "/tmp/dify_holiday_jp_cache.csv"
CACHE_TTL_SECONDS = 86400  # 1日


def _is_cache_valid() -> bool:
    if not os.path.exists(CACHE_FILE):
        return False
    mtime = os.path.getmtime(CACHE_FILE)
    return (time.time() - mtime) < CACHE_TTL_SECONDS


def _fetch_and_cache() -> str:
    response = requests.get(HOLIDAY_CSV_URL, timeout=10)
    response.raise_for_status()
    # Shift-JIS → UTF-8 変換
    text = response.content.decode("shift_jis")
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def _load_cache() -> str:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def get_holiday_map() -> dict[str, str]:
    """
    祝日の辞書を返す。
    キー: "YYYY/M/D" 形式の文字列
    値: 祝日名（日本語）
    """
    if _is_cache_valid():
        text = _load_cache()
    else:
        text = _fetch_and_cache()

    holiday_map: dict[str, str] = {}
    reader = csv.reader(io.StringIO(text))
    for row in reader:
        if len(row) < 2:
            continue
        date_str = row[0].strip()
        name = row[1].strip()
        # ヘッダー行をスキップ
        if date_str == "国民の祝日・休日月日" or not date_str:
            continue
        try:
            # CSV は "YYYY/M/D" 形式
            parsed = datetime.strptime(date_str, "%Y/%m/%d").date()
            holiday_map[parsed.isoformat()] = name
        except ValueError:
            continue

    return holiday_map


def get_holiday_name(target_date: date) -> Optional[str]:
    """
    指定日の祝日名を返す。祝日でなければ None。
    """
    holiday_map = get_holiday_map()
    return holiday_map.get(target_date.isoformat())
