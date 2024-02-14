import os
os.environ["OPENAI_API_KEY"] = "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"
baseDir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, request
import random
from werkzeug.utils import secure_filename
import json
import time
import traceback
import shutil
from flask_cors import CORS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableParallel

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import gc


# document formatter
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# llm
llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)




template = """You are a Chatbot which do automated feedback giver for students. 

Format for Question and Answer is given below.

- Question: A sentence or a paragraph that asks about a specific topic or concept from the given section.
- Answer: A sentence or a paragraph that provides the correct or incorrect answer to the question.
- Mark Count: A number that indicates the maximum mark for the question.
- Is this answer correct? If not, provide the correct answer from the given section. Provide a mark out of the mark count.
- Feedback: Provide feedback on the accuracy and clarity of the answer if full marks were not attained. Additionally, suggest a relevant section or topic to study from context given below if the answer was not fully correct.

Example Number 1. Here Answer is correct and got full marks.
Question: List the three main security properties and briefly describe the purpose of each one.
Answer: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.
Mark Count: 10
Helpful Answer : Your answer is correct.
Total mark for this question: 10/10

Example Number 2. Here Answer is incorrect and got 0 marks.
Question: What is an initial sequence number (ISN)?
Answer: A number used in reconstructing a UDP session
Mark Count: 2
Helpful Answer : Your answer is incorrect.
The correct answer is: A number that indicates where a packet falls in the data stream.
Review section 2.9 TCP session hijacking for more information on ISN.
Total mark for this question: 0/2.

Example Number 3. Here Answer is empty and got 0 marks.
Question: What is an initial sequence number (ISN)?
Answer:
Mark Count: 2
Helpful Answer : Your answer is empty.
The correct answer is: A number that indicates where a packet falls in the data stream.
Review section 2.9 TCP session hijacking for more information on ISN.
Total mark for this question: 0/2.

Example Number 4. Here Answer is partially correct so got 3/10.
Question: List the three main security properties and briefly describe the purpose of each one.
Answer: Confidentiality, Integrity, Availability.
Mark Count: 10
Helpful Answer : You have stated the security properties correctly, but have failed to describe the purpose of each one.
The correct answer is: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.
Re-read section "1.5 How do we define security?" for further information on the topic of security properties
Total mark for this question: 3/10

These Examples are strict pattern to follow, every answer will be in same structure as these example you can answer in any other way.

Context:
{context}

{question}

Helpful Answer:"""

rag_prompt = PromptTemplate.from_template(template)




app = Flask(__name__)
CORS(app)



@app.route('/api/v1/uploadDocuments', methods=['POST'])
def uploadDocuments():
    try:
        if 'file' not in request.files:
            return json.dumps({"message" : "file missing from request"}), 400
        file = request.files['file']
        if file.filename == '':
            return json.dumps({"message" : "file name missing"}), 400
        else:
            filename = secure_filename(file.filename)
            path = os.path.join(baseDir, "static/documents")
            # check if does not exist create a directory
            if not os.path.exists(path):
                os.makedirs(path)

            path = os.path.join(path, filename)
            file.save(path)
            file.close()

            return json.dumps({"message" : "successfully uploaded"}), 200
    except Exception as e:
        return json.dumps({"message" : f"error occured : {str(e)}"}), 500

@app.route('/api/v1/deleteDocuments', methods=['GET'])
def deleteDocuments():
    try:
        try:
            path = os.path.join(baseDir, "static/documents")
            shutil.rmtree(path) 
        except:
            pass 
        
        try:
            faiss_path = os.path.join(baseDir, "static/faiss_index")
            shutil.rmtree(faiss_path)
        except:
            pass

        return json.dumps({"message" : "successfully deleted"}), 200
    
    except Exception as e:

        return json.dumps({"message" : f"error occured : {e} , {traceback.format_exc()}"})


# process document request is for processing uploaded documents so that..
# it creates a knowledge base this request is neccessary after..
# uploading new documents ... 
@app.route('/api/v1/processDocuments', methods=['GET'])
def processDocument():
    try:
        path = os.path.join(baseDir, "static/documents")
        
        # loads the all pdfs from path directory
        loader = DirectoryLoader(path, glob="**/*.pdf")
        docs = loader.load()

        for i in range(len(docs)):
            docs[i].page_content = docs[i].page_content + "*****"
        
        faiss_path = os.path.join(baseDir, "static/faiss_index")

        if not os.path.exists(faiss_path):
            os.makedirs(faiss_path)

        # splits text in 1000 character string with overlap 500
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=3000, chunk_overlap=0, separator="/\\*{5}/", is_separator_regex=True
        )
        
        all_splits = text_splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(all_splits, OpenAIEmbeddings())
        
        vectorstore.save_local(faiss_path)  

        return json.dumps({"message" : "successfully processed documents and added to knowledgebase"}), 200

    except Exception as e:
        
        return json.dumps({"message" : f"error occured : {str(e)}, {traceback.format_exc()}"}), 500


@app.route('/api/v1/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        prompt = data['prompt']

        faiss_path = os.path.join(baseDir, "static/faiss_index")
        vectorstore = FAISS.load_local(faiss_path, OpenAIEmbeddings())
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | rag_prompt
            | llm
            | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)

        response = rag_chain_with_source.invoke(prompt)
        
        print({ "question" : response['question'], 
                            "answer" : response['answer'],
                            "context" : response['context'][0].page_content})

        data = None
        prompt = None
        rag_chain = None
        retriever = None
        vectorstore = None

        gc.collect()

        return json.dumps({ "question" : response['question'], 
                            "answer" : response['answer'],
                            "context" : response['context'][0].page_content}), 200

    except Exception as e:

        return json.dumps({"message" : f"error occured : {str(e)}, {traceback.format_exc()}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0' ,port=8501)



