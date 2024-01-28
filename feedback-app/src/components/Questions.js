import React, { useState } from "react";
import QuizQuestion from "./QuizQuestion";

const Questions = () => {
  const [answers, setAnswers] = useState({});
  const questions = [
    {
      id: 1,
      question: "What is the capital of France?",
      answer: "Paris",
      marks: 5,
    },
    {
      id: 2,
      question: 'Who wrote "To Kill a Mockingbird"?',
      answer: "Harper Lee",
      marks: 10,
    },
  ];

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleFormSubmit = () => {
    // Handle submission of all answers
    console.log("All answers submitted:", answers);
  };

  return (
    <div>
      <h2>Quiz Questions</h2>
      <form onSubmit={handleFormSubmit}>
        {questions.map((question) => (
          <QuizQuestion
            key={question.id}
            question={question.question}
            marks={question.marks}
            questionNumber={question.id}
            onAnswerChange={(answer) => handleAnswerChange(question.id, answer)}
          />
        ))}
        <button className="btn btn-secondary mt-2">Finish</button>
      </form>
    </div>
  );
};

export default Questions;
