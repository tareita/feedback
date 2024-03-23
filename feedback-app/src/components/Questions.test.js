import React from "react";
import {
  render,
  fireEvent,
  waitFor,
  getByTestId,
} from "@testing-library/react";
import Questions from "./Questions";
import { API_URL } from "../config";
import { useGlobal } from "../contexts/Context";
import fetchMock from "jest-fetch-mock";

fetchMock.enableMocks();

jest.mock("../contexts/Context", () => ({
  useGlobal: () => ({
    setTotalMark: jest.fn(), // Provide a mock function for setTotalMark
    feedback: "", // Provide dummy value for feedback
    setFeedback: jest.fn(), // Provide a mock function for setFeedback
  }),
}));
describe("Questions component", () => {
  beforeEach(() => {
    fetchMock.resetMocks(); // Reset fetch mock before each test
  });

  test("renders correctly", () => {
    const { getByText, getByLabelText } = render(<Questions />);

    expect(getByText("Week 1 Quiz")).toBeInTheDocument();
  });

  test("allows selecting file and triggering upload", async () => {
    fetchMock.mockResponse(JSON.stringify({ message: "Documents deleted." })); // Mock API response

    const { getByLabelText } = render(<Questions />);
    const fileInput = getByLabelText("Upload File");

    const file = new File(["test content"], "test.csv", { type: "text/csv" });
    fireEvent.change(fileInput, { target: { files: [file] } });

    // Wait for API call to upload documents
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(API_URL + "api/v1/deleteDocuments", {
        method: "GET",
      });
    });
  });

  test("uploads documents successfully", async () => {
    fetch.mockResponse(JSON.stringify({ message: "Documents uploaded." })); // Mock API response

    const { getByLabelText } = render(<Questions />);
    const fileInput = getByLabelText("Upload File");

    const file = new File(["test content"], "test.csv", { type: "text/csv" });
    fireEvent.change(fileInput, { target: { files: [file] } });

    // Wait for API call to upload documents
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(API_URL + "api/v1/uploadDocuments", {
        method: "POST",
        body: expect.any(FormData),
      });
    });
  });
});
