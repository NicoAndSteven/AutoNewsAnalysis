import requests

# 配置API地址和userToken
api_url = "http://localhost:8000/v1/chat/completions"  # API地址
user_token = "xqUajyaIBfRNd6i2dmKy45fH1QYVXinwwSPhUxqEkvqkOMpe4X82lqIWsxnUiqOO"  # 替换为你的userToken

# 请求头
headers = {
    "Authorization": f"Bearer {user_token}",  # 设置Authorization头
    "Content-Type": "application/json"  # 设置Content-Type为JSON
}

# 请求体
data = {
    "model": "deepseek",  # 模型名称
    "messages": [
        {
            "role": "user",  # 用户角色
            "content": "你好，你能做什么？"  # 用户输入
        }
    ],
    "stream": False  # 是否使用流式响应
}

# 发送POST请求
try:
    response = requests.post(api_url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        result = response.json()
        print("API响应内容:")
        print(result["choices"][0]["message"]["content"])  # 输出助手的回复
    else:
        # 请求失败时的处理
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)

except requests.exceptions.RequestException as e:
    # 处理请求异常
    print("请求发生异常:", e)