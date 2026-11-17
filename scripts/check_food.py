"""data/food.json の書き方をチェックする（GitHub Actions から動く）"""
import json, sys

ALLOWED = {"name", "when", "kind", "area", "budget", "status", "note", "url", "by"}
STATUS = {"候補", "決定", "予約済み", "見送り"}
errors = []
try:
    data = json.load(open("data/food.json", encoding="utf-8"))
except json.JSONDecodeError as e:
    sys.exit(f"JSONの書き方がおかしいです（{e.lineno}行目 {e.colno}文字目）: {e.msg}")
shops = data.get("shops") if isinstance(data, dict) else None
if not isinstance(shops, list):
    sys.exit('いちばん外は {"shops": [ ... ]} の形にしてください')
for i, s in enumerate(shops, 1):
    where = f"{i}件目"
    if not isinstance(s, dict):
        errors.append(f"{where}: {{ }} で囲んでください"); continue
    if not str(s.get("name", "")).strip():
        errors.append(f"{where}: name（店の名前）が空です")
    extra = set(s) - ALLOWED
    if extra:
        errors.append(f"{where}: 知らない項目があります {sorted(extra)}（使えるのは {sorted(ALLOWED)}）")
    if s.get("status") and s["status"] not in STATUS:
        errors.append(f"{where}: status は {sorted(STATUS)} のどれかにしてください")
    if s.get("url") and not str(s["url"]).startswith("https://"):
        errors.append(f"{where}: url は https:// から始まるものにしてください")
    for k, v in s.items():
        if not isinstance(v, str):
            errors.append(f"{where}: {k} は文字（\"〜\"）で書いてください")
        elif len(v) > 300:
            errors.append(f"{where}: {k} が長すぎます（300文字まで）")
if errors:
    print("\n".join(errors)); sys.exit(1)
print(f"OK: {len(shops)}件")
