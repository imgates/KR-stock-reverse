import json
import urllib.request
from datetime import datetime

TARGETS = [
    {"code": "000660", "name": "SK하이닉스", "held": 15, "reduce_target": 11, "avg_price": 2468866},
    {"code": "402340", "name": "SK스퀘어", "held": 11, "reduce_target": 8, "avg_price": 1848188}
]

def fetch_recent_data(item_code):
    url = f"https://m.stock.naver.com/api/stock/{item_code}/price?pageSize=5&page=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        
    history = []
    for d in data:
        history.append({
            "date": f"{d['localTradedAt'][4:6]}.{d['localTradedAt'][6:8]}",
            "close": int(d["closePrice"].replace(",", ""))
        })
    history.reverse()
    return history

def run():
    result = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }
    
    for stock in TARGETS:
        code = stock["code"]
        history = fetch_recent_data(code)
        closes = [h["close"] for h in history]
        
        star_point = round(sum(closes) / len(closes))
        sell_order = ((star_point + 999) // 1000) * 1000
        buy_order = (star_point // 1000) * 1000
        sell_qty = stock["held"] // 10

        result["stocks"][code] = {
            "name": stock["name"],
            "held": stock["held"],
            "reduce_target": stock["reduce_target"],
            "avg_price": stock["avg_price"],
            "sell_qty": sell_qty,
            "star_point": star_point,
            "sell_order": sell_order,
            "buy_order": buy_order,
            "history": history
        }
        
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("data.json 업데이트 완료")

if __name__ == "__main__":
    run()
