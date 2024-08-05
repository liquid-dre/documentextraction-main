import os
from langchain.text_splitter import CharacterTextSplitter
from unstructured.partition.pdf import partition_pdf


# Extract elements from PDF
def extract_pdf_elements(output_file_path, fname):
    """
    Extract images, tables, and chunk text from a PDF file.
    path: File path, which is used to dump images (.jpg)
    fname: File name
    """
    image_path = "./"
    return partition_pdf(output_file_path + fname,
                       extract_images_in_pdf=True,
                       infer_table_structure=True,
                       chunking_strategy="by_title",
                        max_characters=4000,
                        new_after_n_chars=3800,
                        combine_text_under_n_chars=2000,
                         image_output_dir_path=output_file_path
    )


# Categorize elements by type
def categorize_elements(raw_pdf_elements):
    """
    Categorize extracted elements from a PDF into tables and texts.
    raw_pdf_elements: List of unstructured.documents.elements
    """
    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            texts.append(str(element))
    return texts, tables

def extract_and_categorize_pdf(output_file_path, filename):
    # File path
    texts_4k_token =''
    tables = []
    texts = []
    if os.path.exists(output_file_path + filename):
        try:
            # Get elements
            raw_pdf_elements = extract_pdf_elements(output_file_path, filename)

            # Get text, tables
            texts, tables = categorize_elements(raw_pdf_elements)

            # Optional: Enforce a specific token size for texts
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=4000, chunk_overlap=0
            )
            joined_texts = " ".join(texts)
            texts_4k_token = text_splitter.split_text(joined_texts)
        except Exception as e:
            print(f"Error extracting PDF elements: {e}")
    else:
        print(f"File '{fpath}' does not exist.")
        return f"File '{fpath}' does not exist."
    # Should return the text_4k_tokens and tables

    return texts_4k_token, tables, texts

