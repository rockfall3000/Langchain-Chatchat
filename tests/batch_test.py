import time
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

# 请求LLM接口
def get_answer(query):
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    inputBody = {
      "knowledge_base_id": "kb-hr",
      "question": query,
      "history": []
    }
    # pprint(inputBody)

    return requests.post('http://0.0.0.0:7861/local_doc_qa/local_doc_chat', headers = headers, data = json.dumps(inputBody))
    
def test_knowledge_chat(query, kb):
    api_base_url = 'http://0.0.0.0:7861'
    api="/chat/knowledge_base_chat"
    url = f"{api_base_url}{api}"
    data = {
        "query": query,
        "knowledge_base_name": kb,
        "history": [],
        "stream": False 
    }
    dump_input(data, api)
    response = requests.post(url, headers=headers, json=data, stream=True)
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


# embedding_model = SentenceTransformer('/mnt/workspace/bge-large-zh-v1.5')#, device='cuda'

def calc_similarity(str1, str2):
    # multi-qa-MiniLM-L6-cos-v1可以替换成其他语言模型，即使不是sentence tranformers库官方列出的
    # model.encode一行代码即可实现句子向量化
    query_embedding = embedding_model.encode(str1)
    # 可同时输入多个句子，后台按照batch一块推理
    passage_embedding = embedding_model.encode(str2)
    similarity = util.cos_sim(query_embedding, passage_embedding)[0][0]
    print("Similarity:", similarity)
    return similarity


test_file_name = './data/questions-hr.json'
knowledge_base_name = 'kb-hr-1213'
output_file_name = './output/result-'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.csv'

# 从json文件中读取问题集
with open(test_file_name, 'r') as f:
    data = json.load(f)
    pprint('questions count:%d' %len(data))

# 初始化csv文件输出writer
with open(output_file_name, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['question', 'llm_answer', 'similarity', 'standard_answer'])
    # 向LLM提问并将答案输出到csv文件中
    for record in data['questions']:
        # TODO 拼接提示词，考虑由LangChain实现
        real_question = "根据文档《"+record['relatedDoc']+"》，请回答："+record['question']
        print("request with question:"+real_question)
        ret = test_knowledge_chat(real_question, knowledge_base_name)["answer"].replace("\n", "")
        # print(ret)
        # calc_similarity(ret, record['stdAnswer'])
        writer.writerow([real_question, ret, 'null', record['stdAnswer']])
        # time.sleep(10)

