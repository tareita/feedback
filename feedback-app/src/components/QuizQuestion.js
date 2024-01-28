import React, { useState } from "react";
import ".././stylesheets/QuizQuestion.css"; // Importing the CSS file

const QuizQuestion = ({ question, onAnswerSubmit, questionNumber, marks }) => {
  const [answer, setAnswer] = useState("");

  const handleAnswerChange = (e) => {
    setAnswer(e.target.value);
  };

  const handleSubmit = () => {
    onAnswerSubmit(answer, marks);
    setAnswer("");
  };

  return (
    <div className="row my-3">
      <div className="col-md-2">
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">Question {questionNumber}</h5>
            <div className="form-group">
              <label htmlFor="marks">Marked out of:</label>
              <div>{marks}</div>
            </div>
          </div>
        </div>
      </div>
      <div className="col-md-8">
        <div className="card">
          <div className="card-body mb-3">
            <h3 className="card-title">{question}</h3>
            <textarea
              className="form-control"
              value={answer}
              onChange={handleAnswerChange}
              placeholder="Your answer"
              rows={4}
            />
            <button className="btn btn-primary mt-2" onClick={handleSubmit}>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizQuestion;
