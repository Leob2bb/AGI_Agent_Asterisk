from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = f"너가 말한 건: {user_input}"  # 응답 메시지 (임시)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
