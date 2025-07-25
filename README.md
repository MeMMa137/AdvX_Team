# 飞书多维表格数据处理系统

## 简介
本系统用于从飞书多维表格获取用户的姓名和兴趣数据，为拥有相同兴趣的用户建立匹配 ID，并将数据存储到本地 SQLite 数据库。

## 环境准备
1. 安装 Python 3.7 及以上版本。
2. 安装飞书 Python SDK：
   ```bash
   pip install lark-oapi -U
   ```

## 配置步骤
1. 在飞书开发者后台创建企业自建应用或商店应用，获取 `YOUR_APP_ID` 和 `YOUR_APP_SECRET`。
2. 打开 `data_processor.py` 文件，将 `YOUR_APP_ID` 和 `YOUR_APP_SECRET` 替换为实际值。
3. 确保 `app_token` 为正确的值（当前已设置为 `AwaIbS2k6affImsEc9rcCp0mnKh`）。

## 运行项目
在项目根目录下运行以下命令：
```bash
python3 data_processor.py
```

## 数据库结构
数据存储在 `user_data.db` 文件中，包含一个 `users` 表，字段如下：
- `name`: 用户姓名
- `interest`: 用户兴趣
- `match_id`: 匹配 ID