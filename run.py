#!/usr/bin/env python3

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import pprint, os

load_dotenv()

# Define prompt
# https://kubernetes.io/docs/contribute/style/style-guide/
prompt_template = """Given the following style guide: {style_guide_url}

Find violations of the style guide. Even if a page is not part of the style guide's project, look for violations of the style guide and list them out in detail.

If there are no violations for a page, write "NONE"

FILE: 
"{file}"

VIOLATIONS:"""
prompt = PromptTemplate.from_template(prompt_template)
# We want to run an individual LLM query on each file for cleanliness and to avoid hitting a token limit
# This could be optimized in the future
for f in os.getenv('FILES').split('|||'):
    if os.path.isfile(f):
        loader = UnstructuredFileLoader(f)
        docs = loader.load()
    else:
        print(f'Invalid file: {f}')

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, 
                                    document_variable_name="file")
    
    results = stuff_chain.invoke({'input_documents': docs,
                                  'style_guide_url': os.getenv('STYLE_GUIDE_URL')})

    pprint.pprint(results)