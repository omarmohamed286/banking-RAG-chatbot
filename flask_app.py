from flask import Flask, request, jsonify
from rag import Rag
from pathlib import Path
import json

app = Flask(__name__)


def retrieve():
    rag = Rag(Path('config/config.yaml'))
    llm = rag.get_llm()
    prompt = rag.get_prompt()
    retriever = rag.get_retriever()
    return rag.retrieve_from_db(llm, retriever, prompt)


@app.route('/')
def index():
    return jsonify({'msg': 'system is up'})


@app.route('/get_response', methods=['POST'])
def get_response():
    query = request.get_json()['query']
    qa = retrieve()
    response = qa(query)
    answer = response['result']
    source_document = response['source_documents'][0].page_content
    doc = response['source_documents'][0].metadata['source']
    response_data = {"answer": answer,
                     "source_document": source_document, "doc": doc}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
