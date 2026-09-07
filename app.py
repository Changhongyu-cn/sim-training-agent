from flask import Flask, request, jsonify, render_template
from agent_core import run_agent

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    print(f"📩 收到用户问题: {user_input}")  # 1.确认收到请求

    if not user_input:
        return jsonify({"error": "请输入问题"}), 400

    try:
        print("⏳ 正在调用 Agent...")  # 2.确认进入处理
        result = run_agent(user_input)
        print(f"✅ Agent 返回结果: {result}")  # 3.确认处理完成
        return jsonify(result)
    except Exception as e:
        print(f"❌ 发生错误: {e}")  # 4.捕获报错
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)