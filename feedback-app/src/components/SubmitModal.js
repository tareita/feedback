import React from "react";

const SubmitModal = () => {
  return (
    <div>
      <button
        type="button"
        class="btn btn-primary btn-lg"
        data-bs-toggle="modal"
        data-bs-target="#myModal"
      >
        <div className="fw-bold">Finish Attempt...</div>
      </button>
      <div
        class="modal fade"
        id="myModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title title fs-3" id="exampleModalLabel">
                Submit Quiz
              </h1>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
              ></button>
            </div>
            <div class="modal-body">
              Are you sure you would like to submit your answers? No further
              modifications can be made after you submit this attempt.
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Back to attempt
              </button>
              <button
                type="submit"
                class="btn btn-success"
                data-bs-dismiss="modal"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubmitModal;
