import React, { useEffect, useState } from "react";
import QuizQuestion from "./QuizQuestion";
import ".././stylesheets/Questions.css";
import SubmitModal from "./SubmitModal";
import Review from "./Review";
import { API_URL } from "../config";
import questions from "../questions/week1.js";

const Questions = () => {
  const [answers, setAnswers] = useState({});
  const [showCorrectAnswers, setShowCorrectAnswers] = useState(false);
  const [toggleModal, setToggleModal] = useState(true);

  const uploadDocuments = async (files) => {
    const res2 = await fetch(API_URL + "api/v1/deleteDocuments", {
      method: "GET",
    });
    const data1 = await res2.json();
    console.log(data1.message);
    console.log(files);

    // Map each file to a promise that uploads it
    const uploadPromises = files.map((file) => {
      const formData = new FormData();
      formData.append("file", file);
      return uploadHelper(formData); // Return the promise returned by uploadHelper
    });

    // Wait for all uploads to finish
    await Promise.all(uploadPromises);

    processDocuments();
  };

  const uploadHelper = async (formdata) => {
    const res = await fetch(API_URL + "api/v1/uploadDocuments", {
      method: "POST",
      body: formdata,
    });

    const data = await res.json();
    console.log(data.message);
  };

  const processDocuments = async () => {
    const res3 = await fetch(API_URL + "api/v1/processDocuments", {
      method: "GET",
    });
    const data3 = await res3.json();
    console.log(data3.message);
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    uploadDocuments(files);
  };

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
          <input
            class="form-control-file"
            type="file"
            multiple
            onChange={handleFileChange}
            data-testid="form-control-file"
            aria-label="Upload File"
          />
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
