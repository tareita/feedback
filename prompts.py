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
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Mark_Count": "10",
     "Mark_Attained":"10",
     "Feedback": "Your answer is correct."},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality, Integrity, Availability.",
     "Mark_Count": "10",
     "Mark_Attained":"3",
     "Feedback": """You have stated the security properties correctly, but have failed to describe the purpose of each one.
     The correct answer is: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users." 
     Re-read chapter "1.5 How do we define security?" for further information on the topic of security properties"""},
    {"Question": "Briefly explain the following kinds of mechanisms: Deter, Deny, Detect.",
     "Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.",
     "Mark_Count": "3",
     "Mark_Attained": "3",
     "Feedback": "Your answer is correct."},
    {"Question": "Briefly explain the following kinds of mechanisms: Deter, Deny, Detect.",
     "Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access.",
     "Mark_Count": "3",
     "Mark_Attained": "2",
     "Feedback": """Your answer is mainly correct. You have not explained the Detect mechanism. 
     The correct answer is Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.
     Re-read chapter "1.5 How do we define security?" for further information on the security mechanisms. """},
    {"Question": "Briefly explain the following kinds of attacks: jamming, spoofing, hijacking, sniffing, poisoning.",
     "Answer": "",
     "Mark_Count": "5",
     "Mark_Attained": "0",
     "Feedback": """No answer was provided. The correct answer is: Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks."""},
    {"Question": "Briefly explain the following kinds of attacks: jamming, spoofing, hijacking, sniffing, poisoning.",
     "Answer": "Jamming: affecting availability for legitimate packets by 'talking' too much.",
     "Mark_Count": "5",
     "Mark_Attained": "1",
     "Feedback": """You have provided a partial answer. Correct description of jamming, well done! The correct answer is: Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks, specifically spoofing, hijacking, sniffing and poisoning."""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Data Link Layer: routes packets accross diff networks Network Layer: forwards frames in a single network Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Mark_Count": "3",
     "Mark_Attained": "1",
     "Feedback": """Your answer is partially correct. You have correctly defined the Transport Layer., however your Data Link and Network Layer answers are flipped.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology"""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Mark_Count": "3",
     "Mark_Attained": "3",
     "Feedback": "Your answer is correct."},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Transport Layer: transports stuff",
     "Mark_Count": "3",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology"""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "aaaaaaaa",
     "Mark_Count": "3",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology, and reattempt."""},
]
# Function to generate a prompt based on the question-answer pair
def generate_prompt(question, answer, mark_count):
    return f"""Question: {question} Answer: {answer} Mark Count: {mark_count}
    Is this answer correct? If not, provide the correct answer. Provide a mark out of the mark count. Feedback: Provide feedback on the accuracy and clarity of the answer if full marks was not attained. Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct."""

# Function to generate a response based on the mark count
def generate_response(mark_attained, mark_count, feedback):
    return f"""{feedback}
    Total mark for this question: {mark_attained}/{mark_count}"""

def append_to_jsonl(file_path, data):
    with jsonlines.open(file_path, mode='a') as writer:
        writer.write(data)

def clear_jsonl(file_path):
    with open(file_path, mode='w'):
        pass

clear_jsonl("training_data.jsonl")


# Generate and print prompts and responses
for qa_pair in question_answers:
    prompt = generate_prompt(qa_pair["Question"], qa_pair["Answer"], qa_pair["Mark_Count"])
    response = generate_response(qa_pair["Mark_Attained"], qa_pair["Mark_Count"], qa_pair["Feedback"])
    json_entry = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
    append_to_jsonl('training_data.jsonl', json_entry)
    
# ## validation data!
# validated_prompts = [
#     {"Question": "Explain the concept of photosynthesis.",
#      "Answer": "Photosynthesis is the process...",
#      "Mark_Count": "10",
#      "Mark_Attained":"",
#      "Feedback": ""},
#     {"Question": "What is the capital of France?",
#      "Answer": "The capital of France is Paris.",
#      "Mark_Count": "8",
#      "Mark_Attained":"",
#      "Feedback": ""},
# ]

# for qa_pair in validated_prompts:
#     prompt = generate_prompt(qa_pair["Question"], qa_pair["Answer"], qa_pair["Mark_Count"])
#     response = generate_response(
#         qa_pair["Mark_Attained"],
#         qa_pair["Mark_Count"],
#         qa_pair["Feedback"]
#     )
#     json_entry = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
#     append_to_jsonl('validation_data.jsonl', json_entry)
    