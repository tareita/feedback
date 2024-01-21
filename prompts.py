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
     "Correct_Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Feedback": "Your answer is correct."},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality, Integrity, Availability.",
     "Mark_Count": "10",
     "Mark_Attained":"3",
     "Correct_Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Feedback": """You have stated the security properties correctly, but have failed to describe the purpose of each one.
     The correct answer is: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users." 
     Re-read chapter "1.5 How do we define security?" for further information on the topic of security properties"""},
    {"Question": "Briefly explain the following kinds of mechanisms: Deter, Deny, Detect.",
     "Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.",
     "Mark_Count": "3",
     "Mark_Attained": "3",
     "Correct_Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.",
     "Feedback": "Your answer is correct."},
    {"Question": "Briefly explain the following kinds of mechanisms: Deter, Deny, Detect.",
     "Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access.",
     "Mark_Count": "3",
     "Mark_Attained": "2",
     "Correct_Answer": "Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.",
     "Feedback": """Your answer is mainly correct. You have not explained the Detect mechanism. 
     The correct answer is Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorised access. Detect: it monitors for attacks.
     Re-read chapter "1.5 How do we define security?" for further information on the security mechanisms. """},
    {"Question": "Briefly explain the following kinds of attacks: jamming, spoofing, hijacking, sniffing, poisoning.",
     "Answer": "",
     "Mark_Count": "5",
     "Mark_Attained": "0",
     "Correct_Answer": """Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks.""",
     "Feedback": """No answer was provided. The correct answer is: Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks."""},
    {"Question": "Briefly explain the following kinds of attacks: jamming, spoofing, hijacking, sniffing, poisoning.",
     "Answer": "Jamming: affecting availability for legitimate packets by 'talking' too much.",
     "Mark_Count": "5",
     "Mark_Attained": "1",
     "Correct_Answer": """Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks.""",
     "Feedback": """You have provided a partial answer. Correct description of jamming, well done! The correct answer is: Jamming: affecting availability for legitimate packets by 'talking' too much. Spoofing: pretending to be someone else on the Internet. Hijacking: taking over a (network) resource which belongs to someone else. Sniffing: listening to network conversation by parties who are not the intended recipients. Poisoning: corrupting a store of information (e.g., a cache) that is relied upon for future communications.
     Study chapter "1.7 Network Attacks" to solidify your knowledge of network attacks, specifically spoofing, hijacking, sniffing and poisoning."""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Data Link Layer: routes packets accross diff networks Network Layer: forwards frames in a single network Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Mark_Count": "3",
     "Mark_Attained": "1",
     "Correct_Answer": """Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology""",
     "Feedback": """Your answer is partially correct. You have correctly defined the Transport Layer., however your Data Link and Network Layer answers are flipped.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets."""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Mark_Count": "3",
     "Mark_Attained": "3",
     "Correct_Answer": """Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.""",
     "Feedback": "Your answer is correct."},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "Transport Layer: transports stuff",
     "Mark_Count": "3",
     "Mark_Attained": "0",
     "Correct_Answer": "Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology"""},
    {"Question": "Briefly describe the main functions of the transport, network and data link layers of the OSI model.",
     "Answer": "aaaaaaaa",
     "Mark_Count": "3",
     "Mark_Attained": "0",
     "Correct_Answer": "Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology, and reattempt."""},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality: information is not learned by unauthorized principals Integrity: ensures data has not been maliciously altered. Availability:services or data can be accessed when desired.",
     "Mark_Count": "10",
     "Mark_Attained":"10",
     "Correct_Answer": "Confidentiality: information is not learned by unauthorized principals Integrity: ensures data has not been maliciously altered. Availability:services or data can be accessed when desired.",
     "Feedback": "Your answer is correct."},
    {"Question": "Imagine you are a network administrator. You see a familiar IP address pinging the broadcast address. What could be possibly happening in this case?",
      "Answer": "A smurf attack.",
      "Mark_Count": "1",
      "Mark_Attained":"1",
      "Correct_Answer": "A smurf attack.",
      "Feedback": "Your answer is correct."},
    {"Question": "Imagine you are a network administrator. You see a familiar IP address pinging the broadcast address. What could be possibly happening in this case?",
      "Answer": "A man-in-the-middle attack.",
      "Mark_Count": "1",
      "Mark_Attained":"0",
      "Correct_Answer": "A smurf attack.",
      "Feedback": """Your answer is incorrect.
      The correct answer is: A smurf attack.
      Study chapter 2.6 Denial of service: amplification attacks, specifically the different types of Distributed Denial of Service attacks such as smurfing. A Man-in-the-Middle (MITM) attack has to do with ARP spoofing so is incorrect for this question."""},
    {"Question": "Imagine you are a network administrator. You see a familiar IP address pinging the broadcast address. What could be possibly happening in this case?",
      "Answer": "A DNS poisoning attack",
      "Mark_Count": "1",
      "Mark_Attained":"0",
      "Correct_Answer": "A smurf attack.",
      "Feedback": """Your answer is incorrect.
      The correct answer is: A smurf attack.
      Study chapter 2.6 Denial of service: amplification attacks, specifically the different types of Distributed Denial of Service attacks such as smurfing. DNS poisoning attacks are not related to IP addresses."""},
    {"Question": "What is an initial sequence number (ISN)?",
     "Answer": "A number used in reconstructing a UDP session",
     "Mark_Count": "2",
     "Mark_Attained": "0",
     "Correct_Answer": "A number that indicates where a packet falls in the data stream.",
     "Feedback": """Your answer is incorrect.
     The correct answer is: A number that indicates where a packet falls in the data stream.
     Review chapter 2.9 TCP session hijacking for more information on ISN."""},
    {"Question": "What is a SYN-Flooding attack?",
      "Answer": "A DoS attack that can be used jointly with IP spoofing",
      "Mark_Count": "3",
      "Mark_Attained": "3",
      "Correct_Answer": "A DoS attack that can be used jointly with IP spoofing",
      "Feedback": "Your answer is correct."},
    {"Question": "What is a SYN-Flooding attack?",
      "Answer": "An attack that requires a modification of the TCP layer (lever 4 OSI) of the server",
      "Mark_Count": "3",
      "Mark_Attained": "0",
      "Correct_Answer": "A DoS attack that can be used jointly with IP spoofing",
      "Feedback": """Your answer is incorrect.
      The correct answer is: A DoS attack that can be used jointly with IP spoofing.
      Review chapter 2.8 Three-Way Handshake. The SYN-flooding attack does not need modification of the layer, it works by not replying with an ACK code."""},
    {"Question": "What is a DHCP starvation attack?",
     "Answer": "An attack that works by broadcasting DHCP requests with spoofed mac addresses",
     "Mark_Count": "3",
     "Mark_Attained": "3",
     "Correct_Answer": "An attack that works by broadcasting DHCP requests with spoofed mac addresses",
     "Feedback": """Your answer is correct."""},
    {"Question": "What is a DHCP starvation attack?",
     "Answer": "An attack that works by broadcasting DHCP requests",
     "Mark_Count": "3",
     "Mark_Attained": "2",
     "Correct_Answer": "An attack that works by broadcasting DHCP requests with spoofed mac addresses",
     "Feedback": """Your answer is partially correct. You have correctly described DHCP starvation attack, but you missed mentioning the spoofed MAC addresses.
     The correct answer is: An attack that works by broadcasting DHCP requests with spoofed MAC addresses.
     Refer to chapter "2.5 DHCP attacks" for a more detailed understanding."""},
    {"Question": "Explain the term 'IP Spoofing' and its potential impact on network security.",
     "Answer": "IP Spoofing is a technique where an attacker sends IP packets from a false (or 'spoofed') source address to deceive the recipient about the origin of the message. This can lead to unauthorized access and trust exploitation.",
     "Mark_Count": "5",
     "Mark_Attained": "5",
     "Correct_Answer": "IP Spoofing is a technique where an attacker sends IP packets from a false (or 'spoofed') source address to deceive the recipient about the origin of the message. This can lead to unauthorized access and trust exploitation.",
     "Feedback": "Your answer is correct."},
    {"Question": "Define the term 'Firewall' and explain its role in network security.",
     "Answer": "A Firewall is a network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It acts as a barrier between a trusted internal network and untrusted external networks, preventing unauthorized access.",
     "Mark_Count": "6",
     "Mark_Attained": "6",
     "Correct_Answer": "A Firewall is a network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It acts as a barrier between a trusted internal network and untrusted external networks, preventing unauthorized access.",
     "Feedback": "Your answer is correct."},
    {"Question": "What is the purpose of an Intrusion Detection System (IDS) in network security?",
     "Answer": "An Intrusion Detection System (IDS) is designed to monitor network or system activities for malicious actions or policy violations. It detects and responds to potential security threats, providing an additional layer of defense against cyberattacks.",
     "Mark_Count": "4",
     "Mark_Attained": "4",
     "Correct_Answer": "An Intrusion Detection System (IDS) is designed to monitor network or system activities for malicious actions or policy violations. It detects and responds to potential security threats, providing an additional layer of defense against cyberattacks.",
     "Feedback": "Your answer is correct."},
    {"Question": "List and describe the techniques that firewalls use to control access and enforce the site's security policy.",
     "Answer": "Service control: determines the types of Internet services that can be accessed, inbound or outbound. Direction control: determines the direction in which particular service requests may be initiated and allowed to flow through the firewall.\nUser control: controls access to a service according to which user is attempting to access it. Behaviour control: controls how particular services are used.",
     "Mark_Count": "6",
     "Mark_Attained": "6",
     "Correct_Answer": "Service control: determines the types of Internet services that can be accessed, inbound or outbound. Direction control: determines the direction in which particular service requests may be initiated and allowed to flow through the firewall.\nUser control: controls access to a service according to which user is attempting to access it. Behaviour control: controls how particular services are used.",
     "Feedback": """Your answer is correct."""},
    {"Question": "Describe what a VPN is.",
     "Answer": "A virtual private network (VPN) consists of a set of computers connected by means of a relatively insecure network that make use of encryption and special protocols to provide security. It uses encryption and authentication in the lower protocol layers to provide a secure connection through an otherwise insecure network, typically the Internet. Encryption may be performed by firewall software or by routers. Most common protocol mechanism used for this purpose is at the IP level and is known as IPsec.",
     "Mark_Count": "5",
     "Mark_Attained": "5",
     "Correct_Answer": "A virtual private network (VPN) consists of a set of computers connected by means of a relatively insecure network that make use of encryption and special protocols to provide security. It uses encryption and authentication in the lower protocol layers to provide a secure connection through an otherwise insecure network, typically the Internet. Encryption may be performed by firewall software or by routers. Most common protocol mechanism used for this purpose is at the IP level and is known as IPsec.",
     "Feedback": """Your answer is correct."""},
    {"Question": "Explain the differences between knowledge and anomaly detection-based IDSs.",
     "Answer": "A knowledge-based detection system relies on models of malicious behavior (traditionally signatures). It identifies matching entries in the event stream.\nAn anomaly detection system relies on models of normal behavior. It identifies anomalous entries in the event stream.\nThe former can detect known attacks, and the latter can detect unknown attacks.",
     "Mark_Count": "6",
     "Mark_Attained": "6",
     "Feedback": """Your answer is correct."""},
    {"Question": "List and describe the techniques that firewalls use to control access and enforce the site's security policy.",
     "Answer": "Firewalls use magic to protect the site. They cast spells to block evil hackers.",
     "Mark_Count": "8",
     "Mark_Attained": "0",
     "Correct_Answer": """Service control (what): determines the types of Internet services that can be accessed, inbound or outbound.
     Direction control (where): determines the direction in which particular service requests may be initiated and allowed to flow through the firewall.
     User control (who): controls access to a service according to which user is attempting to access it.
     Behaviour control (how): controls how particular services are used.""",
     "Feedback": """Your answer is incorrect.
     The correct answers include: Service control (what): determines the types of Internet services that can be accessed, inbound or outbound.
     Direction control (where): determines the direction in which particular service requests may be initiated and allowed to flow through the firewall.
     User control (who): controls access to a service according to which user is attempting to access it.
     Behaviour control (how): controls how particular services are used.
     Revise chapter 3.3 What is a firewall? for more information. """},
    {"Question": "Describe what a VPN is.",
     "Answer": "A virtual private network (VPN) is a type of sandwich that hackers eat to gain access to secure networks.",
     "Mark_Count": "5",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: A virtual private network (VPN) consists of a set of computers connected by means of a relatively insecure network that make use of encryption and special protocols to provide security. It uses encryption and authentication in the lower protocol layers to provide a secure connection through an otherwise insecure network, typically the Internet. Encryption may be performed by firewall software or by routers. Most common protocol mechanism used for this purpose is at the IP level and is known as IPsec.
     A virtual private network (VPN) is not a sandwich. Revise chapter 3.6 Types of firewalls for more information on VPNs"""},
    {"Question": "Explain the differences between knowledge and anomaly detection-based IDSs.",
     "Answer": "Knowledge-based IDSs detect aliens, and anomaly detection-based IDSs detect ghosts.",
     "Mark_Count": "6",
     "Mark_Attained": "2",
     "Feedback": """Your answer is partially correct. However, it contains inaccuracies.
     A knowledge-based detection system relies on models of malicious behavior (traditionally signatures), not aliens. It identifies matching entries in the event stream.
     An anomaly detection system relies on models of normal behavior, not ghosts. It identifies anomalous entries in the event stream.
     The former can detect known attacks, and the latter can detect unknown attacks."""},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality: keeps secrets. Integrity: maintains honesty. Availability: always accessible.",
     "Mark_Count": "10",
     "Mark_Attained": "3",
     "Feedback": """Your answer is partially correct. However, your descriptions are too simplistic.
     The correct answer is: Confidentiality: it assures that private or confidential information is not disclosed to unauthorized individuals. Integrity: it assures that information and programs are changed only in a specified and authorized manner. Availability: it assures that systems work promptly, and service is not denied to authorized users.
     Re-read chapter "1.5 How do we define security?" for further information on the topic of security properties."""},
    {"Question": "Briefly explain the following kinds of mechanisms: Deter, Deny, Detect.",
     "Answer": "Deter: scares attackers. Deny: says no. Detect: finds bad things.",
     "Mark_Count": "3",
     "Mark_Attained": "1",
     "Feedback": """Your answer is partially correct. However, your descriptions lack detail.
     The correct answer is: Deter: it makes it 'too difficult' or 'not worthwhile' to attack. Deny: it prevents unauthorized access. Detect: it monitors for attacks.
     Re-read chapter "1.5 How do we define security?" for further information on security mechanisms."""},
    {"Question": "Briefly describe the main functions of the transport, network, and data link layers of the OSI model.",
     "Answer": "Data Link Layer: moves data around. Network Layer: connects stuff. Transport Layer: sends things.",
     "Mark_Count": "3",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Data Link Layer: responsible for forwarding frames within a single network. Network Layer: routes packets across different networks. Transport Layer: provides end-to-end connectivity, correcting errors, lost packets, and potentially reordering packets to maintain the relative order of packets.
     Study chapter 1.6 Network Structure, specifically the topic OSI Model and basics of network terminology"""},
    {"Question": "Imagine you are a network administrator. You see a familiar IP address pinging the broadcast address. What could be possibly happening in this case?",
      "Answer": "Someone is playing a game. It's harmless.",
      "Mark_Count": "1",
      "Mark_Attained":"0",
      "Feedback": """Your answer is incorrect.
      The correct answer is: A smurf attack.
      Study chapter 2.6 Denial of service: amplification attacks, specifically the different types of Distributed Denial of Service attacks such as smurfing."""},
    {"Question": "What is an initial sequence number (ISN)?",
     "Answer": "A secret code used for secure communication",
     "Mark_Count": "2",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: A number that indicates where a packet falls in the data stream.
     Review chapter 2.9 TCP session hijacking for more information on ISN."""},
    {"Question": "What is a SYN-Flooding attack?",
      "Answer": "An attack that overwhelms the server by sending too many synchronization requests",
      "Mark_Count": "3",
      "Mark_Attained": "2",
      "Feedback": """Your answer is partially correct. However, you could provide more detail on how the attack works.
      Review chapter 2.8 Three-Way Handshake for a better understanding of SYN-Flooding attacks."""},
    {"Question": "What is a DHCP starvation attack?",
     "Answer": "An attack that causes hunger in the DHCP server, making it unable to allocate IP addresses",
     "Mark_Count": "3",
     "Mark_Attained": "1",
     "Feedback": """Your answer is partially correct. However, it contains inaccuracies.
     The correct answer is: An attack that works by broadcasting DHCP requests with spoofed MAC addresses.
     Refer to chapter "2.5 DHCP attacks" for a more detailed understanding."""},
    {"Question": "Explain the term 'IP Spoofing' and its potential impact on network security.",
     "Answer": "IP Spoofing is a technique where an attacker sends IP packets from a false source address to confuse the recipient. It's like a masked hacker.",
     "Mark_Count": "5",
     "Mark_Attained": "4",
     "Feedback": """Your answer is partially correct. However, the impact could be better explained.
     Review chapter 2.7 IP Spoofing for more information on the potential impact of IP Spoofing on network security."""},
    {"Question": "Define the term 'Firewall' and explain its role in network security.",
     "Answer": "A Firewall is a wall of fire that burns any unauthorized access attempts. It's like a digital superhero.",
     "Mark_Count": "6",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: A Firewall is a network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It acts as a barrier between a trusted internal network and untrusted external networks, preventing unauthorized access.
     Revise chapter 3.3 What is a firewall? for more information."""},
    {"Question": "What is the purpose of an Intrusion Detection System (IDS) in network security?",
     "Answer": "An IDS is like a digital watchdog that barks when it sees something suspicious. It keeps hackers away.",
     "Mark_Count": "4",
     "Mark_Attained": "2",
     "Feedback": """Your answer is partially correct. However, it contains inaccuracies.
     The correct answer is: An Intrusion Detection System (IDS) is designed to monitor network or system activities for malicious actions or policy violations. It detects and responds to potential security threats, providing an additional layer of defense against cyberattacks."""},
]

# Function to generate a prompt based on the question-answer pair
def generate_prompt(question, answer, mark_count, correct_ans=None):
    correct_answer_prompt = f"  which is: {correct_ans}" if correct_ans else ""
    return f"""Question: {question} Answer: {answer} Mark Count: {mark_count}
    Is this answer correct? If not, provide the correct answer{correct_answer_prompt}. Provide a mark out of the mark count. Feedback: Provide feedback on the accuracy and clarity of the answer if full marks were not attained. Additionally, suggest a relevant chapter or topic to study if the answer was not fully correct."""

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
    correct_answer = qa_pair.get("Correct_Answer", None)  # Default to None if "Correct_Answer" is not present
    prompt = generate_prompt(qa_pair["Question"], qa_pair["Answer"], qa_pair["Mark_Count"], correct_answer)
    response = generate_response(qa_pair["Mark_Attained"], qa_pair["Mark_Count"], qa_pair["Feedback"])
    json_entry = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
    append_to_jsonl('training_data.jsonl', json_entry)

    
## validation data!
validated_prompts = [
    {"Question": "Which IPSec mode is normally used when we need host-to-host (end-to-end) protection of data?",
     "Answer": "Transport mode",
     "Mark_Count": "1",
     "Mark_Attained": "1",
     "Feedback": "Your answer is correct."},
    {"Question": "Which IPSec mode is normally used when we need host-to-host (end-to-end) protection of data?",
     "Answer": "Both transport and tunnel mode",
     "Mark_Count": "1",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Transport mode
     Revise chapter 4.3 What is IPSec for more information on this topic."""},
    {"Question": "Which IPSec mode encapsulates the entire IP packet between IPSec nodes?",
     "Answer": "Tunnel mode",
     "Mark_Count": "1",
     "Mark_Attained": "1",
     "Feedback": "Your answer is correct."},
    {"Question": "Which IPSec mode encapsulates the entire IP packet between IPSec nodes?",
     "Answer": "PPP",
     "Mark_Count": "1",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: Tunnel mode
     Revise chapter 4.3 What is IPSec for more information on this topic."""},
    {"Question": "What are the goals that the SSL/TLS protocol aims to achieve?",
     "Answer": "Confidentiality, Authentication, Integrity",
     "Mark_Count": "4",
     "Mark_Attained": "3",
     "Feedback": """Your answer is partially correct.
     The correct answer is: Confidentiality, Authentication, Integrity, Secrecy
     You have not mentioned secrecy in your answer. Revise chapter 4.7 The SSL protocol for a better understanding."""},
    {"Question": "Describe the three main sub-protocols and the underlying concepts of SSL/TLS.",
     "Answer": "I don't know",
     "Mark_Count": "8",
     "Mark_Attained": "0",
     "Feedback": """Your answer is incorrect.
     The correct answer is: SSL/ TLS consists of various sub-protocols, which run on top of TCP:
     - SSL Handshake: initiates, or reinitializes existing, connection. It establishes a channel with the desired channel properties.
     - SSL Record: protocol for sending application data. It describes the way in which application data is compressed, authenticated with a MAC, and the way the resulting payload is encrypted.
     - Other protocols: for renegotiating ciphers and error recovery.
     Underlying concepts:
     - An SSL session is an association between the client and server with an associated state that specifies encryption method, client and server MAC secrets, encryption keys, etc.
     - An SSL connection is basically a secure stream within a session.
     Revise the entirety of Week 4, especially SSL and TLS protocols."""},
    {"Question": "Describe the three main sub-protocols and the underlying concepts of SSL/TLS.",
     "Answer": "SSL/TLS includes various sub-protocols over TCP, like SSL Handshake for connection initiation, SSL Record for application data transmission with compression, MAC authentication, and encryption. Additional protocols manage cipher renegotiation and error recovery. Underlying concepts involve SSL sessions as client-server associations with encryption details and SSL connections as secure streams within sessions.",
     "Mark_Count": "8",
     "Mark_Attained": "8",
     "Feedback": """Your answer is correct."""},
    {"Question": "Describe the three main sub-protocols and the underlying concepts of SSL/TLS.",
     "Answer": "SSL/TLS includes various sub-protocols over TCP, like SSL Handshake for connection initiation, SSL Record for application data transmission with compression, MAC authentication, and encryption. Additional protocols manage cipher renegotiation and error recovery. Underlying concepts involve SSL sessions as client-server associations with encryption details",
     "Mark_Count": "8",
     "Mark_Attained": "7",
     "Feedback": """Your answer is partially correct.
     The correct answer is: SSL/ TLS consists of various sub-protocols, which run on top of TCP:
     - SSL Handshake: initiates, or reinitializes existing, connection. It establishes a channel with the desired channel properties.
     - SSL Record: protocol for sending application data. It describes the way in which application data is compressed, authenticated with a MAC, and the way the resulting payload is encrypted.
     - Other protocols: for renegotiating ciphers and error recovery.
     Underlying concepts:
     - An SSL session is an association between the client and server with an associated state that specifies encryption method, client and server MAC secrets, encryption keys, etc.
     - An SSL connection is basically a secure stream within a session.
     You have forgotten to mention the underlying concept: SSL connections as secure streams within sessions."""},
    {"Question": "Imagine you are a network administrator. You see a familiar IP address pinging the broadcast address. What could be possibly happening in this case?",
      "Answer": "A smurf attack.",
      "Mark_Count": "1",
      "Mark_Attained":"1",
      "Correct_Answer": "A smurf attack.",
      "Feedback": "Your answer is correct."},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Mark_Count": "10",
     "Mark_Attained":"10",
     "Correct_Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Feedback": "Your answer is correct."},
    {"Question": "List the three main security properties and briefly describe the purpose of each one.",
     "Answer": "Confidentiality, Integrity, Availability.",
     "Mark_Count": "10",
     "Mark_Attained":"3",
     "Correct_Answer": "Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users.",
     "Feedback": """You have stated the security properties correctly, but have failed to describe the purpose of each one.
     The correct answer is: Confidentiality: it assures that private or confidential information is not disclosed to unauthorised individuals. Integrity: it assures that information and programs are changed only in a specified and authorised manner. Availability: it assures that systems work promptly, and service is not denied to authorised users." 
     Re-read chapter "1.5 How do we define security?" for further information on the topic of security properties"""},
]
for qa_pair in validated_prompts:
    prompt = generate_prompt(qa_pair["Question"], qa_pair["Answer"], qa_pair["Mark_Count"])
    response = generate_response(qa_pair["Mark_Attained"] ,qa_pair["Mark_Count"], qa_pair["Feedback"])
    json_entry = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
    append_to_jsonl('validation_data.jsonl', json_entry)
    