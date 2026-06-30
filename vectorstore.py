from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from datetime import date , datetime

now = datetime.now()
date = date.today()
time = now.strftime("%I.%M.%S %p")

texts = []
metadatas = []


class _LazyVectorStore:
    """Proxy for a Chroma vector store that defers embedding model
    initialisation until the store is first accessed.  This allows the
    FastAPI process to start and pass webhook verification before the
    22 MB HuggingFace model has finished downloading / loading."""

    def __init__(self):
        self._store = None

    def _get_store(self):
        if self._store is None:
            print("Initialising HuggingFace embeddings and Chroma vector store…")
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            self._store = Chroma(
                collection_name="sample",
                embedding_function=embeddings,
                persist_directory="my_chroma_db",
            )
            print("Vector store ready.")
        return self._store

    # Forward every attribute / method access to the real store so that
    # callers (rag.py) can use `vector_store` exactly as before.
    def __getattr__(self, name):
        return getattr(self._get_store(), name)


vector_store = _LazyVectorStore()


def vector_database_result(text, url):

    if not text:
        return

    # Store more of the article so the digest has real substance to work
    # with. The embedding model (MiniLM) only "sees" ~256 tokens for
    # similarity search, but the full text is still stored/returned for
    # use in the LLM prompt context.
    text = {"Content": text[:2000], "Date": date, "Time": time, "URL": url}

    texts.append(text["Content"])
    metadatas.append({"Date": str(text["Date"]),
                      "Time": str(text["Time"]),
                      "URL": text["URL"]})

    vector_store.add_texts(
        texts=[texts[-1]],
        metadatas=[metadatas[-1]]
    )
