from openai import OpenAI
import time


def deepseek_chat(api_key, message):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个全能助手，能够准确解答用户的问题"},
            {"role": "user", "content": message},
        ],
        stream=False
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    api_key = "sk-efac7546842b4e2abc3be31efbfb9f41"

    message = "请问为什么天空是蓝色的？"
    strat = time.time()
    deepseek_chat(api_key, message)
    end = time.time()

    print(f"deepseek_chat 此次调用花费时间为：{(end - strat):.4f}秒")
