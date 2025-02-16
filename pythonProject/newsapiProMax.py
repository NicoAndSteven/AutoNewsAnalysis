import requests
import os
import re
from newspaper import Article

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

def sanitize_filename(filename):
    """ 清理文件名，移除不允许的字符 """
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def fetch_article_content(url):
    """
    获取新闻网页的正文内容，并将内容保存到项目下的 news 文件夹中
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # 手动下载页面内容（便于添加 UA 和代理）
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析网页内容
        article = Article(url)
        article.download(input_html=response.text)
        article.parse()
        content = article.text.strip()

        # 确保 news 文件夹存在
        news_folder = "news"
        os.makedirs(news_folder, exist_ok=True)

        # 使用文章标题生成安全的文件名；没有标题则使用默认名称
        title = article.title if article.title else "news_article"
        safe_title = sanitize_filename(title)
        file_path = os.path.join(news_folder, f"{safe_title}.txt")

        # 保存正文内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 正文已保存到 {file_path}")

        return content
    except Exception as e:
        print(f"⚠️ 内容提取失败: {e}")
        return None

def fetch_top_headlines(country="us"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "apiKey": "1b9bc1a956cf439a956d145672724762",
        "q": "Trump"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            for i, article in enumerate(data.get("articles", []), start=1):
                content = fetch_article_content(article.get('url'))
                title = article.get('title', f"news_{i}")
                if content:
                    print(f"📰 新闻 {i}: {title}")
                    print(f"📝 描述: {article.get('description')}")
                    print(f"🔗 链接: {article.get('url')}\n")
                    # print(f"\n📖 内容摘要（前100字符）:\n{content[:100]}...")
                else:
                    print("❌ 无法获取正文内容\n")
                    continue


        else:
            print("接口错误:", data.get("message"))

    except requests.exceptions.RequestException as e:
        print("网络请求失败:", e)

if __name__ == "__main__":
    fetch_top_headlines("us")
