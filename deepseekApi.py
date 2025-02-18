import requests
import os
import glob
import datetime
import time
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()
# 获取 user_token
user_token = os.getenv("USER_TOKEN")

if not user_token:
    print("未能从 .env 文件中获取 USER_TOKEN，请检查配置。")
    exit(1)

# 配置API地址和userToken
api_url = "http://localhost:8000/v1/chat/completions"  # API地址

# 请求头
headers = {
    "Authorization": f"Bearer {user_token}",  # 设置Authorization头
    "Content-Type": "application/json"  # 设置Content-Type为JSON
}

# 获取当前日期并格式化
today = datetime.datetime.now().strftime("%Y.%m.%d")

# 输入目录改为 DailyNews 下对应日期的文件夹
input_folder = os.path.join("DailyNews", today)  # DailyNews 下的日期文件夹
output_folder = os.path.join("Analysis", f"{today}-analysis")  # 分析结果保存目录，放在 Analysis 文件夹下

if not os.path.exists(input_folder):
    print(f"输入目录 '{input_folder}' 不存在，请检查目录名称是否正确。")
    exit(1)

# 如果 Analysis 文件夹不存在，则创建
os.makedirs(output_folder, exist_ok=True)

# =================== 遍历txt文件 =====================
txt_files = glob.glob(os.path.join(input_folder, "*.txt"))
if not txt_files:
    print(f"在目录 '{input_folder}' 下未找到任何txt文件。")
    exit(1)

def send_request(prompt):
    """发送请求并返回分析文本"""
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"请求失败，状态码: {response.status_code}错误信息: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

for txt_file in txt_files:
    with open(txt_file, "r", encoding="utf-8") as f:
        news_content = f.read()

    # 构造分析提示，要求模型从政治、成因、影响、未来导向等多个维度进行分析
    prompt = f"请从政治、成因、影响、未来导向等多个维度对以下新闻内容进行全面分析：\n\n{news_content}"

    # 初次请求
    analysis_text = send_request(prompt)

    # 如果返回内容过短，休眠10秒后重试
    if analysis_text and len(analysis_text) < 50:
        print("分析结果过短，可能是服务器繁忙，20秒后重试...")
        time.sleep(20)
        analysis_text = send_request(prompt)

    if analysis_text:
        base_name = os.path.basename(txt_file)
        output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}-analysis.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(analysis_text)
        print(f"分析结果已保存到 '{output_file}'\n")
    else:
        print(f"文件 '{txt_file}' 分析失败。")

