import React, { useState, useEffect } from "react";
import ".././stylesheets/QuizQuestion.css"; // Importing the CSS file
import { API_URL } from "../config";
import { useGlobal } from "../contexts/Context";

const QuizQuestion = ({
  question,
  onAnswerChange,
  questionNumber,
  marks,
  showCorrectAnswer,
}) => {
  const [answer, setAnswer] = useState("");
  const [correctAnswer, setCorrectAnswer] = useState("");
  const { setTotalMark, feedback, setFeedback } = useGlobal();
  const [questionMark, setQuestionMark] = useState(0);
  const [currFeedback, setCurrFeedback] = useState(""); // State to store mark for the current question
  const [loading, setLoading] = useState(false);
  const handleAnswerChange = (e) => {
    setAnswer(e.target.value);
    onAnswerChange(e.target.value);
  };

  const getMarks = (feedback) => {
    const markPattern = /mark\s*for\s*.*?(\d+)\/\d+/i;
    const match = feedback.match(markPattern);
    let mark = null;
    if (match) {
      mark = parseInt(match[1]); // Extracted mark value
    }
    return mark || 0; // Return 0 if no mark found
  };

  const fetchFeedback = async () => {
    const prompt = {
      prompt: "Question:" + question + " Answer:" + answer + " Marks:" + marks,
    };
    const res = await fetch(API_URL + "api/v1/chat", {
      method: "POST",
      body: JSON.stringify(prompt),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await res.json();
    setCorrectAnswer(data.answer);
    const mark = getMarks(data.answer);
    setQuestionMark(mark); // Update mark for the current question
    setCurrFeedback(data.answer);
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
      setFeedback((prevFeedback) => prevFeedback.concat(currFeedback));
      console.log(currFeedback);
      console.log(feedback);
    }
  }, [questionMark, currFeedback, showCorrectAnswer]); // Run effect when questionMark or showCorrectAnswer changes

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

export default QuizQuestion;
