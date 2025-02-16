import requests
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

def fetch_top_headlines(country="us"):
    # NewsAPI 的顶级新闻接口地址
    url = "https://newsapi.org/v2/top-headlines"

    # 设置请求参数：指定国家和 API Key
    params = {
        # "sources": "bbc",
        "country": "us",  # 新闻所属国家（例如 "us" 为美国，"cn" 为中国）
        "apiKey": "1b9bc1a956cf439a956d145672724762",  # 替换成你自己的 API Key
        "q":"Trump"
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)
        # 检查请求是否成功
        response.raise_for_status()
        # 将返回的 JSON 数据转换为 Python 字典
        data = response.json()

        # 如果返回状态为 "ok"，则处理新闻数据
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            for i, article in enumerate(articles, start=1):
                print(f"新闻 {i}: {article.get('title')}")
                print(f"描述: {article.get('description')}")
                print(f"链接: {article.get('url')}\n")
        else:
            print("接口返回错误:", data.get("message"))

    except requests.exceptions.RequestException as e:
        print("请求异常:", e)


if __name__ == "__main__":
    # 获取美国最新的头条新闻
    fetch_top_headlines("us")
