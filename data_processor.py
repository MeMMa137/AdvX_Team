import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
import pandas as pd
from feishu_questionnaire_sdk import get_questionnaire_data

# 从飞书多维表格获取数据
# 修改为使用 SDK 获取问卷信息
def fetch_data_from_feishu():
    response_data = get_questionnaire_data()
    if not response_data:
        lark.logger.info('未获取到飞书数据')
        return []
    records = []
    try:
        lark.logger.info(f'获取到的原始数据: {response_data}')
        # 假设数据在 records 字段中，需根据实际返回结构调整
        if hasattr(response_data, 'items'):
            lark.logger.info(f'items 数量: {len(response_data.items)}')
            for item in response_data.items:
                fields = item.fields if hasattr(item, 'fields') else {}
                name = fields.get('nickname', '')
                interest = fields.get('interest', '')
                # 确保 interest 是字符串类型
                if isinstance(interest, list):
                    interest = ''.join(map(str, interest))
                email = fields.get('email', '')
                records.append((name, interest, email))
        else:
            lark.logger.info('返回数据中没有 items 属性')
    except Exception as e:
        lark.logger.error(f"数据解析失败: {str(e)}")
    lark.logger.info(f'解析后的数据: {records}')
    return records

# 为相同兴趣的用户生成 match_id
def generate_match_ids(users):
    interest_map = {}
    lark.logger.info(f'待生成 match_id 的数据数量: {len(users)}')
    for idx, (name, interest, email) in enumerate(users):
        if interest not in interest_map:
            interest_map[interest] = f"match_{len(interest_map)}"
    result = [(name, interest, email, interest_map[interest]) for name, interest, email in users]
    lark.logger.info(f'生成 match_id 后的数据: {result}')
    return result

# 将数据存储到 Excel 文件
def store_data_to_excel(users):
    lark.logger.info(f'待存储到 Excel 的数据数量: {len(users)}')
    df = pd.DataFrame(users, columns=['name', 'interest', 'email', 'matchid'])
    df.to_excel('user_data.xlsx', index=False)
    lark.logger.info('数据已尝试存储到 user_data.xlsx')

# 主函数
def main():
    lark.logger.info('程序开始执行')
    users = fetch_data_from_feishu()
    users_with_match = generate_match_ids(users)
    store_data_to_excel(users_with_match)
    lark.logger.info('程序执行结束')

if __name__ == "__main__":
    main()