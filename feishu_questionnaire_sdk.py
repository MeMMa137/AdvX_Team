import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


def get_questionnaire_data():
    # 创建客户端，配置鉴权信息
    client = lark.Client.builder() \
        .app_id("cli_a8e5444630b9101c") \
        .app_secret("gJ5012ZVxV0BQMKEWB3tHcTVrTmlX5qu") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象，设置表格和视图信息
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .app_token("AwaIbS2k6affImsEc9rcCp0mnKh") \
        .table_id("tblTETQbFcHlWmLB")\
        .user_id_type("user_id")\
        .page_size(20)\
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id("vewQx72054")
            .field_names(["nickname", "interest", "email"])
            .automatic_fields(True)
            .build()) \
        .build()

    # 发起请求，使用指定的用户访问令牌
    option = lark.RequestOption.builder() \
        .user_access_token("u-cdNPGTM5h8uX_oiirHrEDD4kkI4501GhgMG01hqaGy9z") \
        .build()
    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"获取数据失败，错误码: {response.code}, 错误信息: {response.msg}, "
            f"日志ID: {response.get_log_id()}, 响应内容: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return None

    # 处理并返回业务结果
    return response.data


if __name__ == "__main__":
    # 调用函数获取数据
    questionnaire_data = get_questionnaire_data()
    
    # 打印获取到的数据
    if questionnaire_data:
        lark.logger.info("成功获取问卷数据:")
        lark.logger.info(lark.JSON.marshal(questionnaire_data, indent=4))
