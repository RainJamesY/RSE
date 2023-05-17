import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser

DATA_DIR = "tdt3"
INDEX_DIR = "TDT3_index"

def create_index():
    # 定义Schema
    schema = Schema(docno=ID(stored=True), text=TEXT(stored=True))

    # 创建索引目录
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    # 创建索引
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()

    # 遍历TDT3数据文件
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    docno = get_docno(file_path)  # 提取文档编号
                    writer.add_document(docno=docno, text=content)

    writer.commit()
    print("Index created successfully.")

def get_docno(file_path): # 获取文档序号
    docno = os.path.splitext(os.path.basename(file_path))[0]
    return docno

if __name__ == "__main__":
    # 创建索引
    create_index()

