import React, { useEffect, useState } from "react";
import ".././stylesheets/QuizQuestion.css"; // Importing the CSS file
import { useGlobal } from "../contexts/Context";
import { API_URL } from "../config";

const McqQuestion = ({
  question,
  options,
  marks,
  questionNumber,
  correctAns,
  onAnswerChange,
  showCorrectAnswer,
  section, // Add prop to handle answer change
}) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [answer, setAnswer] = useState("");
  const [correctAnswer, setCorrectAnswer] = useState("");
  const { setTotalMark } = useGlobal();
  const [questionMark, setQuestionMark] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    // Pass selected answer to parent component
    setAnswer(option);
    onAnswerChange(option);
  };

  const fetchFeedback = async () => {
    const prompt = {
      prompt:
        "Question: " +
        question +
        " " +
        "Student Answer: " +
        answer +
        " " +
        "Correct Answer: " +
        correctAns +
        " " +
        "Section: " +
        section,
    };
    const res = await fetch(API_URL + "api/v1/chatMcq", {
      method: "POST",
      body: JSON.stringify(prompt),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    setCorrectAnswer(data.feedback);
    const mark = answer === correctAns ? 1 : 0;
    setQuestionMark(mark); // Update mark for the current question
    setLoading(false);
  };

  useEffect(() => {
    if (showCorrectAnswer) {
      setLoading(true);
      fetchFeedback();
    }
  }, [showCorrectAnswer]); // Run effect when showCorrectAnswer changes

  useEffect(() => {
    if (showCorrectAnswer) {
      setTotalMark((prevTotal) => prevTotal + questionMark); // Update totalMark with mark for the current question
    }
  }, [questionMark, showCorrectAnswer]); // Run effect when questionMark or showCorrectAnswer changes

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
            <ul className="list-group">
              {options.map((option, index) => (
                <li key={index} className="list-group-item">
                  <div className="form-check">
                    <input
                      className="form-check-input"
                      type="radio"
                      id={`option-${index}`}
                      name={`options-${questionNumber}`} // Use unique name for each question
                      value={option}
                      checked={option === selectedOption}
                      onChange={() => handleOptionSelect(option)}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`option-${index}`}
                    >
                      {option}
                    </label>
                  </div>
                </li>
              ))}
            </ul>
            {showCorrectAnswer &&
              (loading ? (
                <div
                  class="spinner-border text-warning spinner-answer"
                  role="status"
                >
                  <span class="sr-only"></span>
                </div>
              ) : (
                <div className="correct-answer">
                  <strong>Feedback:</strong> {correctAnswer}
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default McqQuestion;
