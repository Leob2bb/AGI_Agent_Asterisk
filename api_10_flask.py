from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_URL = "http://apis.data.go.kr/B552016/MaintMngTechService/getMaintMngTechList"
SERVICE_KEY = "u7Vh%2BxEuNlSYY792R5h9Cqe%2BSjpZTksUkUBWRBZiJnWpKaHxMbzWNb%2BzM%2BOaBh0Jsy8atJNOfkyZZVzh6LrmxA%3D%3D"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>유지관리 기술정보</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>유지관리 기술정보</h1>
    {% if items %}
    <table>
        <tr>
            <th>번호</th>
            <th>주제</th>
            <th>기술 분류</th>
            <th>시설 종류</th>
            <th>기관</th>
        </tr>
        {% for item in items %}
        <tr>
            <td>{{ item.no }}</td>
            <td>{{ item.subject }}</td>
            <td>{{ item.techCl }}</td>
            <td>{{ item.facilKind }}</td>
            <td>{{ item.techSource }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>데이터를 불러올 수 없습니다.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "type": "xml"
    }
    try:
        res = requests.get(API_URL, params=params)
        print("응답 상태코드:", res.status_code)
        print("응답 내용:", res.text)  # 여기가 핵심!

        data = res.json()
        items = data['response']['body']['items']['item']
    except Exception as e:
        print("Error:", e)
        items = []
    return render_template_string(HTML_TEMPLATE, items=items)


if __name__ == '__main__':
    app.run(debug=True)
