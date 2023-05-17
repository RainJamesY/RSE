from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.query import Wildcard
from whoosh import scoring
import re
from whoosh.highlight import WholeFragmenter
import numpy as np

DATA_DIR = "TDT3"
INDEX_DIR = "TDT3_index"


def search_amb(query_str, n=10):
    # 打开索引
    ix = index.open_dir(INDEX_DIR)

    # 创建搜索器
    with ix.searcher() as searcher:
        # 创建查询解析器
        query_parser = QueryParser("text", schema=ix.schema)

        # 执行搜索
        results = searcher.search(query_parser.parse(query_str), limit=n)

        # 对结果进行排序
        sorted_results = sorted(results, key=lambda r: r.score, reverse=True)

        hits = []
        for rank, r in enumerate(sorted_results, start=1):
            hit = {
                "rank": rank,
                "score": np.log(r.score),
                "docno": r["docno"],
                "text": r.highlights("text"),
            }
            hits.append(hit)
        return hits


def print_results(hits):
    print("Top {} results:".format(len(hits)))
    for hit in hits:
        print("Rank: {}\tScore: {}\tDocument No.: {}\nSnippet: {}\n".format(
            hit["rank"], hit["score"], hit["docno"], hit["text"]))


def process_query_amb(query_str):
    # 处理查询字符串，提取自由文本和短语查询
    free_text = []
    phrases = []

    # 匹配带引号的短语查询
    quoted_phrases = re.findall(r'"([^"]+)"', query_str)
    phrases.extend(quoted_phrases)

    # 移除带引号的短语查询
    query_str = re.sub(r'"([^"]+)"', '', query_str)

    # 提取自由文本查询
    free_text = query_str.split()

    return free_text, phrases


if __name__ == "__main__":
    # 从命令行读取查询字符串
    query_str = input("Enter your query: ")

    # 处理查询字符串
    free_text, phrases = process_query_amb(query_str)

    # 构建查询字符串
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    # 模糊查询：添加通配符
    query_string = " ".join([term + "*" for term in query_string.split()])

    # 执行搜索
    hits = search_amb(query_string, n=10)
    print_results(hits)
