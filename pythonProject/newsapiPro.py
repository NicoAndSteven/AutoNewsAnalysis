import requests
import os
from newspaper import Article

# 设置代理（根据你的网络环境调整）
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'


def fetch_article_content(url):
    """ 获取新闻网页的正文内容 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # 手动下载页面内容（便于添加UA和代理）
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析网页内容
        article = Article(url)
        article.download(input_html=response.text)
        article.parse()
        return article.text.strip()  # 返回清理后的正文
    except Exception as e:
        print(f"⚠️ 内容提取失败: {e}")
        return None


def fetch_top_headlines(country="us"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        "apiKey": "1b9bc1a956cf439a956d145672724762",
        "q": "Trump"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            for i, article in enumerate(data.get("articles", []), start=1):
                print(f"\n📰 新闻 {i}: {article.get('title')}")
                print(f"📝 描述: {article.get('description')}")
                print(f"🔗 链接: {article.get('url')}")

                # 获取并显示正文
                if content := fetch_article_content(article.get('url')):
                    print(f"\n📖 内容摘要（前200字符）:\n{content[:1000]}...")
                else:
                    print("❌ 无法获取正文内容")
        else:
            print("接口错误:", data.get("message"))

    except requests.exceptions.RequestException as e:
        print("网络请求失败:", e)


if __name__ == "__main__":
    fetch_top_headlines("us")