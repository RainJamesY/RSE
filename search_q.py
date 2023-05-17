from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.query import Term
import re
from whoosh.highlight import WholeFragmenter
import numpy as np

DATA_DIR = "TDT3"
INDEX_DIR = "TDT3_index"


def custom_score_fn(searcher, fieldname, text, matcher):
    # 获取查询词的频率
    query_terms = text.lower().split()
    query_freq = {}
    for term in query_terms:
        query_freq[term] = query_freq.get(term, 0) + 1

    # 获取文档长度
    doc_length = searcher.doc_count_all()

    # 获取文档的词频
    doc_freq = {}
    if isinstance(matcher, Term):
        doc_freq = matcher.weighting.reader().frequency(fieldname, matcher.id())

    # 计算文档相关性分数 (TF * IDF)
    score = 0.0
    for term, query_tf in query_freq.items():
        doc_tf = doc_freq.get(term, 0)

        # 计算逆文档频率 (IDF)
        idf = searcher.idf(fieldname, term)

        # 计算TF * IDF
        tf_idf = (query_tf / doc_length) * idf

        # 累加文档相关性分数
        score += tf_idf

    return score


def search(query_str, n=10):
    # 打开索引
    ix = index.open_dir(INDEX_DIR)

    # 创建搜索器
    with ix.searcher() as searcher:
        # 创建查询解析器
        query_parser = QueryParser("text", schema=ix.schema)
        query = query_parser.parse(query_str)

        # 执行搜索
        results = searcher.search(query, limit=n)

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


def process_query(query_str):
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
    free_text, phrases = process_query(query_str)

    # 构建查询字符串
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    # 执行搜索
    hits = search(query_string, n=10)
    print_results(hits)
