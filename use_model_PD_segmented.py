from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader


def run_query(user_query, temperature = 0, k = 1, model = "gpt-3.5-turbo"):
    persist_directory = "db_PD_segmented"
    embedding = OpenAIEmbeddings()

    vecotrdb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    #user_query = "Ali je za nekomitenta banke, ki želi opraviti transakcijo v znesku 17.000 EUR, nujno potrebno določiti oceno tveganja?"

    #user_query = "Ali drži, da se teroristi financirajo tako iz zakonitih kot iz nezakonitih sredstev ter da predhodno kaznivo dejanje ni potrebno?"

    #user_query = """Katere so faze pranja denarja?
    #več pravilnih odgovorov)
    #(1) Kopičenje.
    #(2) Plasiranje.
    #(3) Prikrivanje.
    #(4) Integracija.
    #(5) Označevanje."""

    #user_query = """Kaj od naštetega je pranje denarja? 
    #(1) Nezakonitim sredstvom ustvariti videz legalnosti.	
    #(2) Pridobivanje denarja ali premoženja.
    #(3) Prikrivanje kaznivega izvora denarja ali premoženja."""

    # retriever = vecotrdb.as_retriever()
    retriever = vecotrdb.as_retriever(search_kwargs={"k": 1})
    docs = retriever.get_relevant_documents(user_query)
    print(len(docs))
    for doc in docs:
        print(doc.metadata)

    #model = "gpt-4"
    #model = "gpt-3.5-turbo"

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=temperature, model=model),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    def process_llm_response(llm_response):
        response = llm_response["result"]
        sources = []
        print(llm_response["result"])
        print("\n\nSources")
        for source in llm_response["source_documents"]:
            print(source.metadata["source"])
            sources.append(source.metadata["source"])

        return (response, sources)

        

    query = user_query
    llm_response = qa_chain(query)
    return process_llm_response(llm_response)