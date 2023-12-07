from pprint import pprint
import json
import csv

import requests

from sentence_transformers import SentenceTransformer, util


def dump_input(d, title):
    print("\n")
    print("=" * 30 + title + "  input " + "="*30)
    pprint(d)


def dump_output(r, title):
    print("\n")
    print("=" * 30 + title + "  output" + "="*30)
    for line in r.iter_content(None, decode_unicode=True):
        print(line, end="", flush=True)


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

data = {
    "query": "请用100字左右的文字介绍自己",
    "history": [
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好，我是人工智能大模型"
        }
    ],
    "stream": True,
    "temperature": 0.7,
}


api_base_url = 'http://0.0.0.0:7861'
api="/chat/chat"

# 请求LLM接口
def test_chat_chat(data):
    url = f"{api_base_url}{api}"
    dump_input(data, api)
    response = requests.post(url, headers=headers, json=data, stream=True)
    dump_output(response, api)
    print("\n")
    print("=" * 30 + api + "  output" + "="*30)
    #pprint(response)
    for line in response.iter_content(None, decode_unicode=True):
        print(line)
        data = json.loads(line)
        if "answer" in data:
            print(data["answer"])
            #print(data["answer"], end="", flush=True)
    assert "docs" in data and len(data["docs"]) > 0
    print("=" * 30 + api + "  responese" + "="*30)
    #pprint(data["docs"])
    assert response.status_code == 200
    return data


# 从json文件中读取问题集
with open('./doc_1.txt', 'r') as f:
    content = f.read()
    real_question = "阅读以下文档：'''"+content+"'''/n请输出整个文档的大纲"
    test_chat_chat(real_question)
