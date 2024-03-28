from langchain.llms import CTransformers
from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from utils import read_yaml


class Rag:
    def __init__(self, config_path):
        self.config = read_yaml(config_path)

    def get_llm(self):
        return CTransformers(
            model=self.config['local_llm_path'],
            model_type="mistral",
            lib="avx2",
        )

    def get_prompt(self):
        prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
        return PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

    def get_retriever(self):
        embeddings = SentenceTransformerEmbeddings(
            model_name=self.config['embedding_model'])
        load_vector_store = Chroma(
            persist_directory=self.config['vector_db_params']['persist_directory'], embedding_function=embeddings)
        return load_vector_store.as_retriever(search_kwargs={"k": 1})

    def retrieve_from_db(self, llm, retriever, prompt):
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
            verbose=True
        )
