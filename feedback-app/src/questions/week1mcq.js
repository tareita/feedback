const mcqQuestions = [
  {
    id: 5,
    question:
      "Which security property ensures that information is not disclosed to unauthorized individuals?",
    options: ["Confidentiality", "Integrity", "Availability", "Authentication"],
    correctAnswer: "Confidentiality",
    marks: 1,
    section: "1.5 How do we define security",
  },
  {
    id: 6,
    question: "Which security concept aims to dissuade potential attackers?",
    options: ["Deterrence", "Denial", "Detection", "Jamming"],
    correctAnswer: "Deterrence",
    marks: 1,
    section: "1.5 How do we define security",
  },
  {
    id: 7,
    question:
      "What type of interception is characterized by capturing messages without modification, making it difficult for IT managers to detect?",
    options: [
      "Active interception",
      "Passive interception",
      "Active denial",
      "Active modification",
    ],
    correctAnswer: "Passive interception",
    marks: 1,
    section: "1.9 Physical Interception",
  },
  {
    id: 8,
    question:
      "What type of attack involves an attacker intercepting packets between two components and taking control of the session between them by inserting their own packet?",
    options: [
      "Jamming attack",
      "Sniffing attack",
      "Spoofing attack",
      "Hijacking attack",
    ],
    correctAnswer: "Hijacking attack",
    marks: 1,
    section: "1.7 Network Attacks",
  },
];

export default mcqQuestions;
