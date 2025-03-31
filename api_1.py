from flask import Flask, render_template_string, request
import requests
import urllib.parse
from api_10_flask import HTML_TEMPLATE

app = Flask(__name__)

# 인증키 인코딩
API_BASE_URL = "http://apis.data.go.kr/B552016/MaintMngTechService/getMaintMngTechList"
API_KEY = "u7Vh%2BxEuNlSYY792R5h9Cqe%2BSjpZTksUkUBWRBZiJnWpKaHxMbzWNb%2BzM%2BOaBh0Jsy8atJNOfkyZZVzh6LrmxA%3D%3D"
SERVICE_KEY = "u7Vh+xEuNlSYY792R5h9Cqe+SjpZTksUkUBWRBZiJnWpKaHxMbzWNb+zM+OaBh0Jsy8atJNOfkyZZVzh6LrmxA=="

# 요청 URL을 통해 json 응답 확인
url = API_BASE_URL + f"?serviceKey={API_KEY}&pageNo=1&numOfRows=1&type=json&subject=건설"
try:
    response = requests.get(url, timeout=5)
    # print(response.text)  
except requests.exceptions.SSLError as e:
    print("SSL 오류 발생:", e)

# 관련 주소 REST API로 불러오기
@app.route('/')
def index():
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "type": "json"
    }
    try:
        res = requests.get(API_BASE_URL, params=params)
        print("응답 상태코드:", res.status_code)
        # print("응답 본문: ", res.text)
        data = res.json()
        # print("응답 JSON:", data)

        # JSON 구조에서 item 리스트 꺼내기
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        if not isinstance(items, list):
            items = [items]  # item이 단일 객체일 경우 리스트로 변환

    except Exception as e:
        print("Error:", e)
        items = []

    return render_template_string(HTML_TEMPLATE, items=items)

if __name__ == '__main__':
    app.run(debug=True)

