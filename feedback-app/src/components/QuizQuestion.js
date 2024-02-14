import React, { useState } from "react";
import ".././stylesheets/QuizQuestion.css"; // Importing the CSS file

const QuizQuestion = ({
  question,
  onAnswerChange,
  questionNumber,
  marks,
  showCorrectAnswer,
  correctAnswer,
}) => {
  const [answer, setAnswer] = useState("");

  const handleAnswerChange = (e) => {
    setAnswer(e.target.value);
    onAnswerChange(e.target.value);
  };

  return (
    <div className="row my-3">
      <div className="col-md-3">
        <div className="card">
          <div className="marks card-body">
            <h5 className="card-title">Question {questionNumber}</h5>
            <div className="form-group">
              <label htmlFor="marks">Marked out of:</label>
              <div>{marks}</div>
            </div>
          </div>
        </div>
      </div>
      <div className="col-md-9">
        <div className="card">
          <div className="question card-body mb-3">
            <h5 className="card-title q-title">{question}</h5>
            <textarea
              className="form-control"
              value={answer}
              onChange={handleAnswerChange}
              placeholder="Your answer"
              rows={4}
            />
            {showCorrectAnswer && (
              <div className="correct-answer">
                <strong>Answer:</strong> {correctAnswer}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizQuestion;
