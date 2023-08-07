import os
import openai
import chromadb
import time
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

import streamlit as st

# streamlit run app.py

from prompts import PromptActor, PromptQuestions, PromptAnswerSetup

from dotenv import load_dotenv
load_dotenv()

api_base = os.getenv("AZURE_OPENAI_BASE")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = "2022-12-01"

openai.api_type = 'azure'
openai.api_key = api_key
openai.api_version = api_version
openai.api_base = api_base

def get_embedding(text, model="text-embedding-ada-002"):
   try:
       text = text.replace("\n", " ")
       return openai.Embedding.create(input = [text], model=model, deployment_id=model)['data'][0]['embedding']
   except:
       # st.write("Embedding sleep")
       time.sleep(5)
       return get_embedding(text)

def get_response(prompt):
    return openai.Completion.create(
        engine="Gpt35Turbo",
        prompt=prompt,
        temperature=0.0,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        request_timeout=3600,
        timeout=3600
    )

starting_tic = time.perf_counter()

loader = PyPDFLoader('NASDAQ_AAPL_2022.pdf')

pages = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(pages)

texts = []
metadata = []
embeddings = []
ids = []
current_id = 0

tic = time.perf_counter()
for doc in docs:
    embeddings.append(get_embedding(doc.page_content))
    texts.append(doc.page_content)
    current_id += 1
    ids.append(str(current_id))
    metadata.append(doc.metadata)
toc = time.perf_counter()
# st.write(f"Embeddings and texts took {toc - tic:0.4f} seconds")

chroma_client = chromadb.Client()

tic = time.perf_counter()
collection = chroma_client.get_or_create_collection(name="annualreport")
collection.add(
    embeddings=embeddings,
    documents=texts,
    metadatas=metadata,
    ids=ids
)
toc = time.perf_counter()
# st.write(f"Creating collection took {toc - tic:0.4f} seconds")

st.title('Investment Banker in a Box')
questions = PromptQuestions()
for query in questions:
    tic = time.perf_counter()
    st.subheader(query)
    search = collection.query(
        query_embeddings=get_embedding(query),
        n_results=3,
    )
    toc = time.perf_counter()
    # st.write(f"Chroma search took {toc - tic:0.4f} seconds")
    prompt = PromptActor().format(response=PromptAnswerSetup(), context=search, question=query)
    tic = time.perf_counter()
    response = get_response(prompt)
    toc = time.perf_counter()
    # st.write(f"API response took {toc - tic:0.4f} seconds")

    formatted_response = response.choices[0].text
    if "'''" in formatted_response:
        formatted_response = formatted_response[formatted_response.index("'''")+3:formatted_response.index("'''", formatted_response.index("'''")+3)]
    else:
        if '"""' in formatted_response:
            formatted_response = formatted_response[0:formatted_response.index('"""')]
    st.markdown(formatted_response.replace('$', '\$').replace('\n', '  \n'))

    with st.expander('Document Response'):
        st.write(response)

    st.divider()

ending_toc = time.perf_counter()
st.write(f"Complete analysis took {ending_toc - starting_tic:0.4f} seconds")
