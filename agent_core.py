from dotenv import load_dotenv
import os
import json
import requests
from elasticsearch import Elasticsearch

# ============ 加载环境变量 ============
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 连接 Elasticsearch（确保已启动）
es = Elasticsearch("http://localhost:9200")

# ============ 定义工具 ============
def get_recent_training_data(n=50):
    """获取最近 n 条训练数据"""
    try:
        query = {"query": {"match_all": {}}, "size": n, "sort": [{"timestamp": "desc"}]}
        result = es.search(index="sim_logs", body=query)
        hits = result['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"查询失败: {str(e)}"

def get_training_stats():
    """获取训练统计数据（总条数、平均 reward）"""
    try:
        total = es.count(index="sim_logs")['count']
        avg_reward = es.search(index="sim_logs", body={"size": 0, "aggs": {"avg_reward": {"avg": {"field": "reward"}}}})
        avg = avg_reward['aggregations']['avg_reward']['value']
        return f"总数据条数: {total}, 平均 Reward: {avg:.4f}"
    except Exception as e:
        return f"统计失败: {str(e)}"

# 工具注册表
tools = {
    "get_recent_training_data": get_recent_training_data,
    "get_training_stats": get_training_stats,
        }

# ============ 调用 DeepSeek API ============
def call_deepseek(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
               }
    # 定义工具描述（符合 OpenAI 函数调用格式）
    tool_definitions = [
        {
            "type": "function",
            "function": {
                "name": "get_recent_training_data",
                "description": "获取最近n条训练数据",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "n": {"type": "integer", "description": "数据条数，默认50"}
                                  },
                    "required": []
                              }
                        }
          },
        {
            "type": "function",
            "function": {
                "name": "get_training_stats",
                "description": "获取训练统计数据（总条数、平均reward）",
                "parameters": {"type": "object", "properties": {}}
                         }
        }
    ]
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.3,
        "tools": tool_definitions,
        "tool_choice": "auto"
            }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

# ============ Agent 主逻辑 ============
def run_agent(user_input):
    messages = [
        {"role": "system", "content": "你是一个仿真训练数据分析助手，可以使用工具回答用户问题。"},
        {"role": "user", "content": user_input}
                ]
    while True:
        resp = call_deepseek(messages)
        if "choices" not in resp or not resp["choices"]:
            return f"API错误: {resp}"
        message = resp["choices"][0]["message"]
        if message.get("tool_calls"):
            # 执行工具调用
            tool_call = message["tool_calls"][0]
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            if func_name in tools:
                result = tools[func_name](**args)
                # 将助手消息和工具结果加入对话
                messages.append(message)
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": result})
            else:
                return f"未知工具: {func_name}"
            # 再次调用模型获取最终回答
            resp2 = call_deepseek(messages)
            if "choices" in resp2 and resp2["choices"]:
                return resp2["choices"][0]["message"]["content"]
            else:
                return f"模型错误: {resp2}"
        else:
            return message.get("content", "无回答")

# ============ 测试 ============
if __name__ == "__main__":
    print("🤖 训练数据Agent已启动（原生API版），输入问题或输入exit退出")
    while True:
        user_input = input("\n你: ")
        if user_input.lower() == "exit":
            break
        try:
            answer = run_agent(user_input)
            print(f"Agent: {answer}")
        except Exception as e:
            print(f"错误: {e}")