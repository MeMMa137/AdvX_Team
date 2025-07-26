import sys
sys.path.append('/Users/shorpen/编程/dogprotecter')
from AI_test import request_body, url, headers, sample_path
import requests
import os
import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

# 飞书文档相关配置
DOCUMENT_ID = "IWzRdO9tzoIjoOxV8PbcW60pnD3"
BLOCK_ID = "IWzRdO9tzoIjoOxV8PbcW60pnD3"
USER_ID = "e9121a78"
USER_ACCESS_TOKEN = "u-eNkDJQYi9ebE3EsxRfP_mdkk14ggg1wVii0011w022T7"

# 创建飞书 client
client = lark.Client.builder()\
    .enable_set_token(True) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()

# 读取 sample 文件内容
def read_sample_text():
    with open(sample_path, 'r', encoding='utf-8') as f:
        return f.read()

# 将 sample 文本作为用户的一轮对话添加到 messages
def get_ai_reply():
    sample_text = read_sample_text()
    request_body["messages"].append(
        {"sender_type":"USER", "sender_name":"小明", "text":sample_text}
    )
    
    # 调用 AI 分析数据
    response = requests.post(url, headers=headers, json=request_body)
    response_data = response.json()
    if "reply" in response_data:
        return response_data['reply']
    print("未获取到 AI 回答，请检查 API 响应。")
    return ""

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
    return response

if __name__ == "__main__":
    ai_reply = get_ai_reply()
    if ai_reply:
        create_feishu_doc_block(ai_reply)