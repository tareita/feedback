# """user message:
#     Question: "Example question".
#     Answer: "Example answer"
#     Mark Count: ???
#     Mark: Is this answer correct? Provide a mark out of the mark count
#     Feedback: Provide feedback on the accuracy and clarity of the answer.
#     Provide the correct answer, if answer was not fully correct.
#     Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct.
# """

# """response:
#     Mark/Markcount
#     If incorrect: 
#     Feedback
# """

import json
import jsonlines


# Sample question-answer pairs with specified mark counts
question_answers = [
    {"Question": "Explain the concept of photosynthesis.",
     "Answer": "Photosynthesis is the process...",
     "Mark_Count": "10",
     "Mark_Attained":"",
     "Feedback": ""},
    {"Question": "What is the capital of France?",
     "Answer": "The capital of France is Paris.",
     "Mark_Count": "8",
     "Mark_Attained":"",
     "Feedback": ""},
]

# Function to generate a prompt based on the question-answer pair
def generate_prompt(question, answer, mark_count):
    return f"""Question: {question} Answer: {answer} Mark Count: {mark_count}
    Is this answer correct? If not, provide the correct answer. Provide a mark out of the mark count. Feedback: Provide feedback on the accuracy and clarity of the answer if full marks was not attained. Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct.
"""

# Function to generate a response based on the mark count
def generate_response(mark_attained, mark_count, feedback):
    return f"""{feedback}
    Total mark for this question: {mark_attained}/{mark_count}
"""

def append_to_jsonl(file_path, data):
    with jsonlines.open(file_path, mode='a') as writer:
        writer.write(data)
        
# Generate and print prompts and responses
for qa_pair in question_answers:
    prompt = generate_prompt(qa_pair["Question"], qa_pair["Answer"], qa_pair["Mark_Count"])
    response = generate_response(
        qa_pair["Mark_Attained"],
        qa_pair["Mark_Count"],
        qa_pair["Feedback"]
    )
    json_entry = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
    append_to_jsonl('training_data.jsonl', json_entry)
    
