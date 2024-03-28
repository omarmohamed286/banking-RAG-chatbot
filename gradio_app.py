import gradio as gr
import requests


API_URL = 'http://localhost:5000/get_response'

headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
}


def main(Question):
    response = requests.post(
        API_URL, json={'query': Question}, headers=headers)
    answer = response.json().get('answer')
    source_document = response.json().get('source_document')
    doc = response.json().get('doc')
    return f"answer: {answer} \n \n source_document: {source_document} \n \n doc: {doc}"


demo = gr.Interface(
    fn=main,
    inputs=["text"],
    outputs=["text"],
    title='Banking Chatbot'
)


demo.launch()
