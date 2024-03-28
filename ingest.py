import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from pathlib import Path
from utils import read_yaml


class DataIngestion:
    def __init__(self, config_path):
        self.config = read_yaml(config_path)

    def get_embeddings(self):
        return SentenceTransformerEmbeddings(model_name=self.config['embedding_model'])

    def split_data(self):
        data_splitting_params = self.config['data_splitting_params']
        loader = DirectoryLoader(
            data_splitting_params['data_path'], glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=data_splitting_params['chunk_size'], chunk_overlap=data_splitting_params['chunk_overlap'])
        return text_splitter.split_documents(documents)

    def store_data(self, splitted_documents, embeddings):
        vector_db_params = self.config['vector_db_params']
        Chroma.from_documents(splitted_documents, embeddings,
                              collection_metadata=vector_db_params['collection_metadata'], persist_directory=vector_db_params['persist_directory'])


ingest = DataIngestion(Path('config/config.yaml'))

embeddings = ingest.get_embeddings()
splitted_documents = ingest.split_data()
ingest.store_data(splitted_documents=splitted_documents, embeddings=embeddings)
