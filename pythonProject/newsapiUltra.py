import requests
import os
import re
from newspaper import Article
from datetime import datetime, timedelta

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

def sanitize_filename(filename):
    """ 清理文件名，移除不允许的字符 """
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def fetch_article_content(url):
    """
    获取新闻网页的正文内容，并将内容保存到项目下的按日期命名的文件夹中
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

        # 获取当前系统时间，作为文件夹名称
        current_date = datetime.now().strftime('%Y.%m.%d')
        folder_path = os.path.join(os.getcwd(), current_date)

        # 确保日期命名的文件夹存在
        os.makedirs(folder_path, exist_ok=True)

        # 使用文章标题和发布时间生成安全的文件名
        title = article.title if article.title else "news_article"

        safe_title = sanitize_filename(title)
        file_path = os.path.join(folder_path, f"{safe_title}.txt")

        # 保存正文内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 正文已保存到 {file_path}")

        return content
    except Exception as e:
        print(f"⚠️ 内容提取失败: {e}")
        return None

def fetch_top_headlines(country="us", days=7):
    """
    获取过去指定天数内的新闻头条
    """
    # 计算从今天起几天前的日期
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "apiKey": "1b9bc1a956cf439a956d145672724762",
        "q": "Trump",
        "from": from_date,  # 限制新闻来源日期
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
                else:
                    print("❌ 无法获取正文内容\n")
                    continue

        else:
            print("接口错误:", data.get("message"))

    except requests.exceptions.RequestException as e:
        print("网络请求失败:", e)

if __name__ == "__main__":
    fetch_top_headlines("us", days=7)  # 获取过去7天的新闻
