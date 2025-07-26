import requests
import readline
import os

group_id = "1735365593646764292"
api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLliJjpqoHlpZQiLCJVc2VyTmFtZSI6IuWImOmqgeWllCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxNzM1MzY1NTkzNjU1MTUyOTAwIiwiUGhvbmUiOiIxODg1MTc1MTAxNCIsIkdyb3VwSUQiOiIxNzM1MzY1NTkzNjQ2NzY0MjkyIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDctMjYgMTQ6MjQ6MzEiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.TNknTBz51V9fvSXunm8vye3vnj4XD9LB6udEcz9TRyo82JYCUdtVaz8wMGQYkSIMF40yAQYSGJBndefcai0ymVn-BOljajS76vZsUp6GxNSRymUdF5XJ5OqaIzG9fcOHGsV9MsWIWz4qaPMpE-zFkX87j4T0SHhsX7KSSEpeCe3I5ar3145C0IokdZKH9B2M6DpKzA7PN7V-zVPWJsLJMrSrKZj7iOBSJU1W4Bq4oGUZASQ6UHG3SncKYkOq4jeCB3zbjiGixBf5NKEh7XFpOVY4FfEu2B65w1xLweMu8rL8fRB8iU2Eqx5NFu1TY8-nCC4bsxLnikhuSaOl_BiMwQ"


url = f"https://api.minimaxi.com/v1/text/chatcompletion_pro?GroupId={group_id}"
headers = {"Authorization":f"Bearer {api_key}", "Content-Type":"application/json"}

# tokens_to_generate/bot_setting/reply_constraints可自行修改
request_body = payload = {
    "model":"MiniMax-Text-01",
    "tokens_to_generate":8192,
    "reply_constraints":{"sender_type":"BOT", "sender_name":"Kairos"},
    "messages":[],
    "bot_setting":[
        {
            "bot_name":"Kairos",
            "content":"Kairos是一个思想储存助手。kairos可以总结用户输入的文本信息，判断总结里面灵感生成的片刻，然后总结相应的灵感，并且生成围绕灵感需要进一步所做的执行操作。",
        }
    ],
}

# 读取 sample 文件内容
sample_path = os.path.join(os.path.dirname(__file__), "sample", "sample1")
with open(sample_path, 'r', encoding='utf-8') as f:
    sample_text = f.read()

# 将 sample 文本作为用户的一轮对话添加到 messages
request_body["messages"].append(
    {"sender_type":"USER", "sender_name":"小明", "text":sample_text}
)

response = requests.post(url, headers=headers, json=request_body)
response_data = response.json()
if "reply" in response_data:
    print(f"AI 回答: {response_data['reply']}")
else:
    print("未获取到 AI 回答，请检查 API 响应。")
# 添加循环完成多轮交互
while True:
    # 下面的输入获取是基于python终端环境，请根据您的场景替换成对应的用户输入获取代码
    line = input("发言:")
    # 将当次输入内容作为用户的一轮对话添加到messages
    request_body["messages"].append(
        {"sender_type":"USER", "sender_name":"小明", "text":line}
    )
    response = requests.post(url, headers=headers, json=request_body)
    reply = response.json()["reply"]
    print(f"reply: {reply}")
    #  将当次的ai回复内容加入messages
    request_body["messages"].extend(response.json()["choices"][0]["messages"])
