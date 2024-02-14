import React, { useState } from "react";
import QuizQuestion from "./QuizQuestion";
import ".././stylesheets/Questions.css";
import SubmitModal from "./SubmitModal";
import Review from "./Review";

const Questions = () => {
  const [answers, setAnswers] = useState({});
  const [showCorrectAnswers, setShowCorrectAnswers] = useState(false);
  const [toggleModal, setToggleModal] = useState(true);
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
    {
      id: 3,
      question: 'Who wrote "To Kill a Mockingbird"?',
      answer: "Harper Lee",
      marks: 10,
    },
    {
      id: 4,
      question: 'Who wrote "To Kill a Mockingbird"?',
      answer: "Harper Lee",
      marks: 10,
    },
  ];

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    setShowCorrectAnswers(true);
    setToggleModal(false);
  };

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-6">
          <h2 className="title">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              fill="currentColor"
              className="bi bi-check2-square mx-1"
              viewBox="0 0 16 16"
            >
              <path d="M3 14.5A1.5 1.5 0 0 1 1.5 13V3A1.5 1.5 0 0 1 3 1.5h8a.5.5 0 0 1 0 1H3a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5h10a.5.5 0 0 0 .5-.5V8a.5.5 0 0 1 1 0v5a1.5 1.5 0 0 1-1.5 1.5z" />
              <path d="m8.354 10.354 7-7a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0" />
            </svg>
            Week 1 Quiz
          </h2>
          <form onSubmit={handleFormSubmit}>
            {questions.map((question) => (
              <QuizQuestion
                key={question.id}
                question={question.question}
                marks={question.marks}
                questionNumber={question.id}
                onAnswerChange={(answer) =>
                  handleAnswerChange(question.id, answer)
                }
                showCorrectAnswer={showCorrectAnswers}
                correctAnswer={question.answer}
              />
            ))}
            {toggleModal ? <SubmitModal /> : <div></div>}
          </form>
        </div>
        <div className="col-md-6">
          {!toggleModal ? <Review /> : <div></div>}
        </div>
      </div>
    </div>
  );
};

export default Questions;
