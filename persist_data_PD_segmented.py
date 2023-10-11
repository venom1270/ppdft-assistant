from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
import time

from bs4 import BeautifulSoup
import requests
import re

print("Loading documents...")
loader = DirectoryLoader("docs/pranje_denarja_segmented", glob="**/*.txt")
doc = loader.load()
print(len(doc))

print("Splitting documents...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
texts = text_splitter.split_documents(doc)

print(len(texts))


persist_directory = "db_PD_segmented"
embedding = OpenAIEmbeddings()


total_length = len(texts)
batch_size = 512

for batch_start in range(0, total_length, batch_size):
    batch_end = min(batch_start + batch_size, total_length)
    batch_texts = texts[batch_start:batch_end]
    vectordb = Chroma.from_documents(
        documents=batch_texts,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print(f"Inserted {batch_end}/{total_length} chunks")
    time.sleep(10)



