import os
from langchain.chat_models import ChatOpenAI
import openai
import PyPDF2
from dotenv import load_dotenv

###pdf fed directly to model, doesnt use vector store
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')


def extract_text_from_pdf(pdf_path):
    doc = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len((doc.pages))):
        page = doc.pages[page_num]
        text += page.extract_text()
    return text

def generate_openai_response(user_input, pdf_text):
    # Function to generate OpenAI response for a given user input and PDF text
    # prompt = f"Your PDF text goes here: {pdf_text}\nUser input: {user_input}"
    
    # # Call the OpenAI API to generate a response
    # openai_response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo-1106",  # You can use "text-davinci-002" or "text-davinci-003" for GPT-3.5-turbo
    #     messages=prompt,
    #     max_tokens=256,  # Adjust as needed
    #     temperature=0.5  # Adjust as needed
    # )
    
    user_msg = pdf_text + "\n\n" + user_input
    system_msg = "You are an automated feedback giver for students."

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal::8jTDArZL",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    print(response.choices[0].message.content)
    # return openai_response.choices[0].text.strip()


def truncate_text(text, max_tokens=5000):
    # Truncate the text to fit within the specified token limit
    tokens = text.split()
    truncated_tokens = tokens[:max_tokens]
    print(len(tokens))
    truncated_text = ' '.join(truncated_tokens)
    return truncated_text

def process_folder(folder_path, user_input):
    # Process all PDFs in the given folder
    combined_pdf_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            pdf_text = extract_text_from_pdf(pdf_path)
            combined_pdf_text += pdf_text

    # Generate OpenAI response using the combined PDF text
    truncated_combined_text = truncate_text(combined_pdf_text)
    generate_openai_response(user_input, truncated_combined_text)
    #print(f"Combined PDFs OpenAI Response: {openai_response}\n{'='*50}")



# Example usage
pdf_folder_path = r"C:\Users\Tareita Nawaz\Downloads\feedback\body"
user_input = "Question: What is a SYN-Flooding attack? Answer: An attack that requires a modification of the TCP layer (lever 4 OSI) of the server Mark Count: 3\n    Is this answer correct? If not, provide the correct answer from the given chapters. Provide a mark out of the mark count. Feedback: Provide feedback on the accuracy and clarity of the answer if full marks were not attained. Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct."
process_folder(pdf_folder_path, user_input)
