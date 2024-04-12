import os
baseDir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, request, render_template
import random
from werkzeug.utils import secure_filename
import json
import time
import traceback
import shutil
from openai import OpenAI
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

client = OpenAI()
# document formatter
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# llm
llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0)




template = """You are a Chatbot which is an automated feedback giver for students. 

Format for Question and Answer is given below.

- Question: A sentence or a paragraph that asks about a specific topic or concept from the given section.
- Answer: A sentence or a paragraph that provides the correct or incorrect answer to the question.
- Mark Count: A number that indicates the maximum mark for the question.
- Is this answer correct? If not, provide the correct answer from the given section. Provide a mark out of the mark count.
- Feedback: Provide feedback on the accuracy and clarity of the answer if full marks were not attained. Additionally, suggest a relevant section or topic to study from context given below if the answer was not fully correct.

Example Number 1. Here Answer is empty and got 0 marks.
Question: What is an initial sequence number (ISN)?
Answer:
Mark Count: 2
Helpful Answer : Your answer is empty.
The correct answer is: A number that indicates where a packet falls in the data stream.
Review section 2.9 TCP session hijacking for more information on ISN.
Total mark for this question: 0/2.

Example Number 2. Here Answer is correct and got full marks.
Question: List the three main security properties and briefly describe the purpose of each one.
Answer: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.
Mark Count: 10
Helpful Answer : Your answer is correct.
Total mark for this question: 10/10

Example Number 3. Here Answer is incorrect and got 0 marks.
Question: What is an initial sequence number (ISN)?
Answer: A number used in reconstructing a UDP session
Mark Count: 2
Helpful Answer : Your answer is incorrect.
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

These Examples are STRICT patterns to follow, every answer will be in same structure as these examples you can NOT answer in any other way.

Context:
{context}

{question}

Helpful Answer:"""

rag_prompt = PromptTemplate.from_template(template)

mcqTemplate = """You will be given a question and a student's attempt answer to the question, along with the actual correct answer for
the given question. You will also be given the chapter name of the section that the student needs to focus on. Based on the option the student selected,
tell them if they are correct or incorrect. If they are correct, meaning if the students answer == correct answer, simply say 'Your answer is correct'. If they are incorrect, then tell them the correct answer, which will be given to you. And tell them to review the relevant section given.
Example: Your answer is incorrect. The correct answer is xyz. Refer to chapter x for more information on the topic of ....
Refer to the student as You.
Question, Answer, Correct Answer and Section :"""


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

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
        vectorstore = FAISS.load_local(faiss_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

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

@app.route('/api/v1/feedbackSummary', methods=['POST'])
def feedbackSummary():
    try :
        data = request.json
        prompt = data['prompt']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to create a feedback summary"},
                {"role": "user", "content": "Based on the feedback given below, create a feedback summary of topics the student needs to work on in a paragraph format, refer to the student directly using 'you' in second person. DO NOT refer to question numbers at all! If there is nothing to work on, reply with 'No additional feedback. Keep up the good work!." + prompt}
            ]
        )
        return json.dumps({"feedback" : response.choices[0].message.content})
    except Exception as e:
        return json.dumps({"message" : f"error occured : {str(e)}, {traceback.format_exc()}"}), 500

@app.route('/api/v1/chatMcq', methods=['POST'])
def chatMcq():
    try :
        data = request.json
        prompt = data['prompt']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to mark questions"},
                {"role": "user", "content": mcqTemplate + prompt}
            ]
        )
        return json.dumps({"feedback" : response.choices[0].message.content})
    except Exception as e:
        return json.dumps({"message" : f"error occured : {str(e)}, {traceback.format_exc()}"}), 500
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0' ,port=8501)



