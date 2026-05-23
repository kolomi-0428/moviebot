from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# 暫時先用假資料測試
fake_movies = {
    "限制級": [
        {"title": "奪魂鋸", "hyperlink": "https://example.com/saw"},
        {"title": "恐怖旅舍", "hyperlink": "https://example.com/hostel"}
    ],
    "輔12級": [
        {"title": "復仇者聯盟", "hyperlink": "https://example.com/avengers"}
    ],
    "普遍級": [
        {"title": "玩具總動員", "hyperlink": "https://example.com/toystory"}
    ],
    "保護級": [
        {"title": "小小兵", "hyperlink": "https://example.com/minions"}
    ],
    "輔15級": [
        {"title": "死侍", "hyperlink": "https://example.com/deadpool"}
    ]
}

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(force=True)
        
        # 取得 action 和參數
        action = req.get("queryResult", {}).get("action")
        
        if action == "rateChoice":
            rate = req.get("queryResult", {}).get("parameters", {}).get("rate")
            
            if not rate:
                return make_response(jsonify({"fulfillmentText": "請告訴我要查詢哪種分級的電影，例如：限制級"}))
            
            # 用假資料查詢
            movies = fake_movies.get(rate, [])
            
            if movies:
                result = f"您查詢的 {rate} 電影有：\n"
                for m in movies:
                    result += f"• {m['title']}\n"
                    result += f"  介紹：{m['hyperlink']}\n\n"
            else:
                result = f"抱歉，目前沒有 {rate} 的電影資料"
            
            return make_response(jsonify({"fulfillmentText": result}))
        
        return make_response(jsonify({"fulfillmentText": "我不明白您的意思"}))
    
    except Exception as e:
        return make_response(jsonify({"fulfillmentText": f"發生錯誤：{str(e)}"}))

# Vercel 需要這個 handler
def handler(request):
    return app(request)
