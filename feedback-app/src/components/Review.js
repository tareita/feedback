import React from "react";

const Review = () => {
  return (
    <div>
      <h2 className="mb-3 title">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="32"
          height="28"
          fill="currentColor"
          class="bi bi-search mx-1"
          viewBox="0 0 16 16"
        >
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
        </svg>
        Review
      </h2>
      <div class="card">
        <div class="card-body">
          <h4 className="title">Total Mark: </h4>
          <div>(Placeholder) 10/10 100.00% </div>
          <div>Well done, you have successfully passed this quiz.</div>
          <button className="btn btn-danger my-2">Reattempt quiz</button>
        </div>
      </div>
    </div>
  );
};

export default Review;
