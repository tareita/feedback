# Trit Project

Trit is a chatbot that utilizes RAG (Retrieval-Augmented Generation) and FAISS (Fast Approximate Nearest Neighbor Search) to answer questions based on a collection of PDF documents. The main steps include:

1. Load all the PDF documents from a given directory using DirectoryLoader.
2. Append a separator (*****) to the end of each document’s page content.
3. Split the documents into chunks of 3000 characters each using CharacterTextSplitter.
4. Embed the chunks into vectors using OpenAIEmbeddings and store them in a FAISS index using FAISS.from_documents.
5. Save the FAISS index locally using vectorstore.save_local.
6. Define a rag_chain that takes a question and a context as inputs and returns an answer using rag_prompt and llm.
7. Define a retriever that uses the FAISS index to find the most similar chunk to a given question using vectorstore.as_retriever.
8. Define a rag_chain_with_source that combines the retriever and the rag_chain to answer questions based on the PDF documents using RunnableParallel.
9. Define a chat function that takes a question as input and returns a JSON response with the question, the answer, and the context using rag_chain_with_source.invoke.

## Docker Usage

To run this project using Docker, follow these steps:

1. Build the docker image:

    ```bash
    docker build --network=host -t trit .
    ```

2. Run the docker image:

    ```bash
    docker run -p 8501:8501 trit
    ```

    To run the docker image in detached mode, add -d to the command:

    ```bash
    docker run -d -p 8501:8501 trit
    ```

Alternatively, you can pull the image from Docker Hub:

```bash
docker pull pydashninja/trit
```

## Getting Started

These instructions will guide you on how to set up and run the project locally.

### Prerequisites

Make sure you have the following installed:

- Python
- langchain-openai
- pypdf
- pypdf2
- faiss-cpu
- langchain 
- openai
- tiktoken
- flask
- flask_cors
- unstructured==0.7.12
- pdfminer.six
- pillow
- pdf2image

### Installation

1. **Unzip:**

    ```bash
    unzip the code & go into directory
    ```

2. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

    The application will start running at [http://localhost:8501/](http://localhost:8501/).

2. **Endpoints:**

   - **Upload Documents:**
     - Endpoint: `/api/v1/uploadDocuments`
     - Method: `POST`
     - Description: Upload documents to the server.

   - **Delete Documents:**
     - Endpoint: `/api/v1/deleteDocuments`
     - Method: `GET`
     - Description: Delete uploaded documents from the server.

   - **Process Documents:**
     - Endpoint: `/api/v1/processDocuments`
     - Method: `GET`
     - Description: Process uploaded documents and add them to the knowledge base.

   - **Chat:**
     - Endpoint: `/api/v1/chat`
     - Method: `POST`
     - Description: Engage in a chat with the model based on user input.




