from flask import Flask, request, jsonify, render_template
import search_q
from search_q import search, process_query
from search_q_pure_text import search_text, process_query_text
from search_q_amb import search_amb, process_query_amb
from search_q_stem import search_stem, process_query_stem
import build_idx

app = Flask(__name__, template_folder='templates_folder', static_folder='static')

def format_results(hits):
    results = []
    for hit in hits:
        result = {
            "rank": hit["rank"],
            "score": hit["score"],
            "docno": hit["docno"],
            "snippet": hit["text"]
        }
        results.append(result)
    return results

@app.route('/')
def home():
    return render_template('index.html')

# search matched words
@app.route('/search', methods=['POST'])
def search_handler():
    query_str = request.form.get('query', '')
    n = int(request.form.get('n', 10))

    free_text, phrases = process_query(query_str)
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    hits = search(query_string, n=n)
    results = format_results(hits)

    return render_template('results.html', query=query_str, results=results)

# search matched texts
@app.route('/search_text', methods=['POST'])
def search_handler_text():
    query_str = request.form.get('query', '')
    n = int(request.form.get('n', 10))

    free_text, phrases = process_query_text(query_str)
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    hits = search_text(query_string, n=n)
    results = format_results(hits)

    return render_template('results.html', query=query_str, results=results)

# search with ambiguity
@app.route('/search_amb', methods=['POST'])  # add ambiguous matching
def search_handler_amb():
    query_str = request.form.get('query', '')
    n = int(request.form.get('n', 10))

    free_text, phrases = process_query_amb(query_str)
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    hits = search_amb(query_string, n=n)
    results = format_results(hits)

    return render_template('results.html', query=query_str, results=results)

# search by stemming
@app.route('/search_stem', methods=['POST'])  # add stemming option
def search_handler_stem():
    query_str = request.form.get('query', '')
    n = int(request.form.get('n', 10))

    free_text, phrases = process_query_stem(query_str)
    query_string = " ".join(free_text)
    for phrase in phrases:
        query_string += ' "{}"'.format(phrase)

    hits = search_stem(query_string, n=n)
    results = format_results(hits)

    return render_template('results.html', query=query_str, results=results)

# build index
@app.route('/build-index', methods=['POST'])
def build_index():
    build_idx.create_index()
    return render_template('built.html')

if __name__ == '__main__':
    app.run(debug=True)
