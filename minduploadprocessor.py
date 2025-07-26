import requests
import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
import os

from ai_to_feishu import ai_reply

# MINIMAX 配置
GROUP_ID = "1735365593646764292"
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLliJjpqoHlpZQiLCJVc2VyTmFtZSI6IuWImOmqgeWllCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxNzM1MzY1NTkzNjU1MTUyOTAwIiwiUGhvbmUiOiIxODg1MTc1MTAxNCIsIkdyb3VwSUQiOiIxNzM1MzY1NTkzNjQ2NzY0MjkyIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDctMjYgMTQ6MjQ6MzEiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.TNknTBz51V9fvSXunm8vye3vnj4XD9LB6udEcz9TRyo82JYCUdtVaz8wMGQYkSIMF40yAQYSGJBndefcai0ymVn-BOljajS76vZsUp6GxNSRymUdF5XJ5OqaIzG9fcOHGsV9MsWIWz4qaPMpE-zFkX87j4T0SHhsX7KSSEpeCe3I5ar3145C0IokdZKH9B2M6DpKzA7PN7V-zVPWJsLJMrSrKZj7iOBSJU1W4Bq4oGUZASQ6UHG3SncKYkOq4jeCB3zbjiGixBf5NKEh7XFpOVY4FfEu2B65w1xLweMu8rL8fRB8iU2Eqx5NFu1TY8-nCC4bsxLnikhuSaOl_BiMwQ"
MINIMAX_URL = f"https://api.minimaxi.com/v1/text/chatcompletion_pro?GroupId={GROUP_ID}"
MINIMAX_HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
MINIMAX_MODEL = "MiniMax-Text-01"

# 飞书文档相关配置
DOCUMENT_ID = "IWzRdO9tzoIjoOxV8PbcW60pnD3"
BLOCK_ID = "IWzRdO9tzoIjoOxV8PbcW60pnD3"
USER_ID = "e9121a78"
USER_ACCESS_TOKEN = "t-g1047qjJBWPJFDJTIVJBAH6H7SZRW5IAAGPV4GTH"

# 创建飞书 client
client = lark.Client.builder()\
    .enable_set_token(True) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()

def read_sample_text(): 
    """读取 sample 文件夹中的文本文件"""
    sample_dir = os.path.join(os.path.dirname(__file__), "sample") 
    sample_texts = [] 
    for filename in os.listdir(sample_dir): 
        if os.path.isfile(os.path.join(sample_dir, filename)): 
            with open(os.path.join(sample_dir, filename), 'r', encoding='utf-8') as f: 
                sample_texts.append(f.read()) 
    return "\n".join(sample_texts) 

def call_minimax_api(text: str) -> str: 
    """调用 MINIMAX API 分析文本"""
    request_body = { 
        "model": MINIMAX_MODEL, 
        "tokens_to_generate": 8192, 
        "reply_constraints": {"sender_type": "BOT", "sender_name": "Kairos思想助手"}, 
        "messages": [], 
        "bot_setting": [ 
            { 
                "bot_name": "Kairos", 
                "content": "Kairos是一个思想储存助手。kairos可以总结用户输入的文本信息，判断总结里面灵感生成的片刻，然后总结相应的灵感，并且生成围绕灵感需要进一步所做的执行操作。文档格式应当包括标题，对对话内容的一句话总结，按逻辑总结，灵感捕捉，执行建议以及日程规划。", 
            } 
        ], 
    } 
    
    # 将文本内容作为用户的一轮对话添加到messages 
    request_body["messages"].append( 
        {"sender_type": "USER", "sender_name": "用户", "text": text} 
    ) 
    
    response = requests.post(MINIMAX_URL, headers=MINIMAX_HEADERS, json=request_body) 
    response.raise_for_status() 
    ai_reply = response.json()["reply"] 
    print(f"AI 返回结果: {ai_reply}") 
    return ai_reply 

def create_feishu_doc_block(content: str):
    """在飞书文档中创建块"""
    print(f"尝试创建飞书文档块，内容: {content}")
    # 构造请求对象
    request: CreateDocumentBlockChildrenRequest = CreateDocumentBlockChildrenRequest.builder()\
        .document_id(DOCUMENT_ID) \
        .block_id(BLOCK_ID) \
        .document_revision_id(-1) \
        .user_id_type("user_id") \
        .request_body(CreateDocumentBlockChildrenRequestBody.builder() \
            .children([Block.builder() \
                .block_type(2) \
                .text(Text.builder() \
                    .style(TextStyle.builder() \
                        .build()) \
                    .elements([TextElement.builder() \
                        .text_run(TextRun.builder() \
                            .content(content) \
                            .text_element_style(TextElementStyle.builder() \
                                .bold(False) \
                                .italic(False) \
                                .strikethrough(False) \
                                .underline(False) \
                                .inline_code(False) \
                                .build()) \
                            .build()) \
                        .build()]) \
                    .build()) \
                .build()]) \
            .index(0) \
            .build()) \
        .build()

    # 发起请求
    content = ai_reply
    option = lark.RequestOption.builder().user_access_token(USER_ACCESS_TOKEN).build()
    response: CreateDocumentBlockChildrenResponse = client.docx.v1.document_block_children.create(request, option)

    # 处理失败返回
    if not response.success(): 
        lark.logger.error( 
            f"client.docx.v1.document_block_children.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}") 
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    print(f"飞书文档块创建结果: {response}")
    print(f"飞书文档块创建原始返回: {response.raw.content.decode('utf-8')}")
    return response

def mind_upload_process(text: str):
    """主处理函数，调用 MINIMAX API 并将结果写入飞书文档"""
    ai_result = call_minimax_api(text)
    return create_feishu_doc_block(ai_result)

if __name__ == "__main__":
    sample_text = read_sample_text()
    result = mind_upload_process(sample_text)
    print(result)