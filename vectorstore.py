from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from datetime import date , datetime

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

now = datetime.now()
date = date.today()
time = now.strftime("%I.%M.%S %p")

vector_store = Chroma(
    collection_name="sample",
    embedding_function=embeddings,
    persist_directory="my_chroma_db"
)

texts = []
metadatas = []

def vector_database_result(text,url):

    if not text:
        return
    
    text = {"Content":text[:1000],"Date":date,"Time":time,"URL":url}
    
    texts.append(text["Content"])
    metadatas.append({"Date": str(text["Date"]) ,
                       "Time":str(text["Time"]) ,
                       "URL": text["URL"]})
        
    vector_store.add_texts(
        texts=[texts[-1]],
        metadatas=[metadatas[-1]]
    )

