from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from chains_and_vars import final_chain, embedder

def RAG(page_info,instruction):
  #loading faze
  loader = [Document(page_content=page_info)]
  #indexing.splitting
  splitter = RecursiveCharacterTextSplitter(chunk_size=1200, 
                                          chunk_overlap=200)
  splits = splitter.split_documents(loader)
  #embedding
  #vector db plus retrieval mechanism/engine
  vector_db = FAISS.from_documents(splits, embedder)
  relevant_info = vector_db.max_marginal_relevance_search(instruction,1)
  response = final_chain.run(context=relevant_info,question=instruction)
  del vector_db
  return response
