import json
from .extract_and_categorize_pdf import extract_and_categorize_pdf
from .generate_image_summaries import generate_img_summaries
from .multivector_retriever import create_multi_vector_retriever
from .construct_rag_chain import multi_modal_rag_chain
from .generate_text_and_tables_summaries import generate_text_and_table_summaries
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import base64
import tempfile
import os
import uuid
import re
import json

def base64_to_pdf(base64_string):
  """Converts a base64 encoded string to a PDF and returns the temp directory and filename.

  Args:
    base64_string: The base64 encoded string.

  Returns:
    A tuple containing the temporary directory path and the PDF filename.
  """

  try:
    # Decode the base64 string
    pdf_data = base64.b64decode(base64_string)

    # Get the current working directory
    current_dir = os.getcwd()

    #current_dir = current_dir + '\\processedfiles\\'
    
    # Create a temporary directory within the current working directory
    temp_dir = tempfile.mkdtemp(dir=current_dir)

    # Generate a unique filename
    filename = f"temp_pdf_{uuid.uuid4()}.pdf"

    # Create the full path
    full_path = os.path.join(temp_dir, filename)

    # Write the PDF data to the file
    with open(full_path, 'wb') as f:
      f.write(pdf_data)

    return temp_dir, filename

  except Exception as e:
    print(f"Error converting base64 to PDF: {e}")
    return None, None


def run_document_analysis(base64_encoded_pdf, prompt_description):
 #check valid base64pdf
    temp_dir, filename = base64_to_pdf(base64_encoded_pdf)

    fpath = temp_dir + '\\' #"C:\\Users\\Tinomu\\Downloads\\documentextraction-main\\documentextraction-main\\multimodal\\content\\"
    fname = filename
    texts_4k_token, extracted_tables, extracted_texts = extract_and_categorize_pdf(fpath,fname)

    # # Get text, table summaries
    text_summaries, table_summaries = generate_text_and_table_summaries(
        texts_4k_token, extracted_tables, summarize_texts=True
    )


    # Image summaries
    ''' function is called with the directory path containing the images. This generates base64-encoded images 
    and summaries for each image, utilizing the GPT-4 Vision model for image summarization
    '''
    img_base64_list, image_summaries = generate_img_summaries(fpath)


    ''' Function takes various summaries and corresponding raw contents as input, including text
    summaries, text contents, table summaries, table contents, image summaries, and image base64-encoded strings
    '''
    # Create retriever
    # The vectorstore to use to index the summaries
    vectorstore = Chroma(
        collection_name="rag-storage", embedding_function=OpenAIEmbeddings()
    )

    retriever_multi_vector_img = create_multi_vector_retriever(
        vectorstore,
        text_summaries,
        extracted_texts,
        table_summaries,
        extracted_tables,
        image_summaries,
        img_base64_list,
    )


    # Step 5
    chain_multimodal_rag = multi_modal_rag_chain(retriever_multi_vector_img)


    #Step 6
    '''
    The get_relevant_documents method of the retriever is used to retrieve relevant documents based on the query, with a limit of 6 documents specified.
    '''

    query = "Can you give me a brief description on the document and extract information on the document"

    if prompt_description != '':
        query = prompt_description
        
    docs = retriever_multi_vector_img.get_relevant_documents(query, limit=6)
    len(docs)

    response = chain_multimodal_rag.invoke(query)
    cleaned_json = response.strip("\"\`").replace("\\", "")
    data = cleaned_json.replace("json", "").replace("\n", "").replace("\\", "")

    return json.dumps(data)

