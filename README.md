# documentextraction-main

# Document Extraction and Multimodal RAG

This project involves extracting text, tables, and images from PDF files, and integrating these elements into a multimodal Retrieval-Augmented Generation (RAG) process.

## Prerequisites

Virtual Environment: To isolate dependencies, it's recommended to use a virtual environment. [Learn more about virtual environments.](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

## Setting Up the Environment

### Create a Virtual Environment
python3 -m venv .venv

### Activate the Virtual Environment

#### MacOS/Linux:
source .venv/bin/activate

#### Windows:
.venv\Scripts\activate

### Sidenote
In your code editor, ensure the virtual environment interpreter is selected. In VSCode, press Cmd+Shift+P, then select Python: Select Interpreter.

## Managing Database Migrations

### Create Migrations for Database Models and Tables

python manage.py makemigrations multimodal
python manage.py migrate

### Create a Superuser for Django Admin
python manage.py createsuperuser
Example credentials: username: admin, password: 1234

### Running the Server
To start the Django development server:
python manage.py runserver

## Managing Dependencies

### Install Dependencies
To install all required packages:
pip install -r requirements.txt

### Update Dependencies
To update the requirements.txt file with the current environment:
pip freeze > requirements.txt

### Remove Dependencies
To uninstall all dependencies:
pip uninstall -r requirements.txt -y

## Dockerization

### Dockerize the Application
To containerize the application using Docker, [follow this guide](https://adeniyekehinde0.medium.com/practicing-django-with-docker-on-vscode-7cb179bd241e).

### Build the Docker Image
docker build -t documentextraction-main .

### Potential Issues with Package Installation
If you encounter issues with specific packages like pillow_heif, install them separately:
pip install --no-cache-dir pillow_heif

### Run the Docker Container
docker run -p 8001:8000 documentextraction-main

## Understanding Multimodal RAG

Multimodal RAG integrates text, images, and documents into retrieval and generation processes. This allows conversational agents to generate responses based on both text and visual context.

## Key Steps:
    1. Extract text, tables, and images from PDF files.
    2. Categorize the extracted elements.
    3. Generate summaries for text elements using OpenAI models.
    4. Encode images as base64 strings and summarize them.
    5. Create  a multi-vector retriever for indexing summaries and raw contents.
    6. Initialize a vector store with OpenAI embeddings.
    7. Construct a multimodal RAG chain.
    8. Retrieve relevant documents based on user queries.
    9. Generate responses using the multimodal RAG chain.

## Chunking Strategies
[API Reference for Chunking](https://docs.unstructured.io/api-reference/api-services/chunking)
[Best Practices for Chunking in RAG](https://unstructured.io/blog/chunking-for-rag-best-practices)

## References

[Langchain PDF Document Loader](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/)
[Langchain GitHub Issues](https://github.com/langchain-ai/langchain/issues/16315)
