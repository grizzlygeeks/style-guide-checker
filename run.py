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

If the document does not adhere to the style guide, write "VIOLATIONS FOUND" at the end of your response. Otherwise, write "VALID DOCUMENT" at the end of your response.

If the document is blank, write only write "BLANK DOCUMENT" at the end of your response.

FILE: 
"{file}"

VIOLATIONS:"""
prompt = PromptTemplate.from_template(prompt_template)
# We want to run an individual LLM query on each file for cleanliness and to avoid hitting a token limit
# This could be optimized in the future
override_files = os.getenv('OVERRIDE_FILES')
if override_files is not None:
    changed_files = override_files
else:
    changed_files = os.getenv('FILES')

if changed_files is None or changed_files == '':
    print('No files to process')
    exit(0)

output = {}

for f in changed_files.split('|||'):
    f = f.strip()
    if os.path.isfile(f):
        loader = UnstructuredFileLoader(f)
        docs = loader.load()
    else:
        print(f'Invalid file: `{f}`')
        continue

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, 
                                    document_variable_name="file")
    
    results = stuff_chain.invoke({'input_documents': docs,
                                  'style_guide_url': os.getenv('STYLE_GUIDE')})

    output[f] = results['output_text']

exit_code = 0
for k,v in output.items():
    print(f'FILE: {k}')
    print(v)
    print('\n\n')

    if 'VIOLATIONS FOUND' in v:
        exit_code = 1

exit(exit_code)