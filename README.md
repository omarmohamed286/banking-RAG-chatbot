# Banking-RAG-Chatbot

This is a RAG app that uses neural-chat-7b intel's open source model as LLM and pubmedbert as embedding model, also Chroma DB is used as vector database.
RAG is done using langchain, the model is finally served by a flask app and dealing with model can be done through a gradio app for UI.

## Usage

To run the flask api:

```python flask_app.py```

To run the gradio app:

```gradio gradio_app.py```



