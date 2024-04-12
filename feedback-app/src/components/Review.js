import React, { useState, useEffect } from "react";
import { useGlobal } from "../contexts/Context";
import { API_URL } from "../config";
import ".././stylesheets/QuizQuestion.css";

const Review = () => {
  const { totalMark, feedback } = useGlobal();

  const [review, setReview] = useState("");
  const [percentage, setPercentage] = useState(null);
  const [totalMarkStabilized, setTotalMarkStabilized] = useState(false);
  const [summary, setSummary] = useState("");
  const [feedbackStabilized, setFeedbackStabilized] = useState(false);
  const [loading, setLoading] = useState(false);

  const generateFeedbackSummary = async (feedback) => {
    setLoading(true);
    if (feedbackStabilized) {
      const prompt = {
        prompt: feedback,
      };
      const res = await fetch(API_URL + "api/v1/feedbackSummary", {
        method: "POST",
        body: JSON.stringify(prompt),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await res.json();
      setSummary(data.feedback);
    }
  };

  useEffect(() => {
    let timerId;

    const generateReview = () => {
      if (totalMarkStabilized) {
        if (percentage < 40) {
          setReview(
            "You did not meet the passing threshold for this quiz. We recommend revisiting the module materials and attempting the quiz again to enhance your understanding."
          );
        } else if (percentage >= 40 && percentage < 70) {
          setReview(
            "Congratulations on passing the quiz! However, there is room for improvement in your understanding of the material. We suggest reviewing the indicated chapters in the feedback to strengthen your knowledge further."
          );
        } else if (percentage === 100) {
          setReview(
            "Impressive achievement! You have demonstrated mastery of the material, achieving a flawless score of 100% on the quiz."
          );
        } else if (percentage >= 70) {
          setReview(
            "Well done! You have exhibited a comprehensive understanding of the material and performed well on the quiz with only a few minor improvements needed."
          );
        } else {
          setReview(""); // Default case, if the percentage falls outside the expected range
        }
      }
    };

    if (!timerId) {
      timerId = setTimeout(() => {
        const calculatedPercentage = ((totalMark / 32) * 100).toFixed(2);
        setPercentage(calculatedPercentage);
        setTotalMarkStabilized(true);
        generateReview();
        setFeedbackStabilized(true);
        generateFeedbackSummary(feedback);
        setLoading(false);
      }, 5000); // Adjusted timeout to 5 seconds
    }

    return () => clearTimeout(timerId);
  }, [
    totalMark,
    totalMarkStabilized,
    percentage,
    feedback,
    feedbackStabilized,
  ]);

  return (
    <div>
      <h2 className="mb-5 title">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="32"
          height="28"
          fill="currentColor"
          className="bi bi-search mx-1"
          viewBox="0 0 16 16"
        >
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
        </svg>
        Review
      </h2>
      <div className="card">
        <div className="card-body">
          <h4 className="title">Total Mark: {totalMark}/32</h4>
          <h5 className="font-weight-bold">
            {percentage !== null && `${percentage}%`}
          </h5>
          <div className="mb-3">{review}</div>
          <h5>Feedback summary:</h5>
          {loading ? (
            <div
              class="spinner-border text-warning spinner-answer"
              role="status"
              aria-label="spinner"
            >
              <span class="sr-only"></span>
            </div>
          ) : (
            <div className="correct-answer">{summary !== "" && summary}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Review;
