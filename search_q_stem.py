from whoosh import index
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import Term
from whoosh import scoring
from whoosh.highlight import WholeFragmenter
import numpy as np
import re
from nltk.stem import SnowballStemmer

DATA_DIR = "TDT3"
INDEX_DIR = "TDT3_index"

# 初始化词干提取器
stemmer = SnowballStemmer("english")  # 根据需求选择适当的语言

class StemmingQueryParser(QueryParser):
    def create_term(self, fieldname, text, boost=1.0):
        term = super().create_term(fieldname, text, boost)
        term = term.apply(stemmer.stem)  # 应用词干提取器
        return term

def search_stem(query_str, n=10):
    # 打开索引
    ix = index.open_dir(INDEX_DIR)

    # 创建搜索器
    with ix.searcher() as searcher:
        # 创建查询解析器
        query_parser = StemmingQueryParser("text", schema=ix.schema, group=OrGroup)
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


def process_query_stem(query_str):
    free_text = []
    phrases = []

    quoted_phrases = re.findall(r'"([^"]+)"', query_str)
    phrases.extend(quoted_phrases)

    query_str = re.sub(r'"([^"]+)"', '', query_str)

    free_text = query_str.split()

    # 词干提取
    free_text = [stemmer.stem(word) for word in free_text]

    return free_text, phrases


if __name__ == "__main__":
    # 从命令行读取查询字符串
    query_str = input("Enter your query: ")

    # 处理查询字符串
    free_text, phrases = process_query_stem(query_str)

    # 构建查询字符串
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    # 执行搜索
    hits = search_stem(query_string, n=10)
    print_results(hits)
