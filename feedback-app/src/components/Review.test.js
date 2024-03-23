import React from "react";
import { render, waitFor } from "@testing-library/react";
import Review from "./Review";
import { useGlobal } from "../contexts/Context";
import { API_URL } from "../config";

jest.mock("../contexts/Context", () => ({
  useGlobal: jest.fn(), // Mock the useGlobal hook
}));

describe("Review component", () => {
  beforeEach(() => {
    jest.clearAllMocks(); // Clear all mock implementations before each test
  });

  test("renders total mark correctly", () => {
    useGlobal.mockReturnValue({ totalMark: 20, feedback: "" }); // Mock the useGlobal hook
    const { getByText } = render(<Review />);
    expect(getByText("Total Mark: 20/28")).toBeInTheDocument();
  });

  test("renders feedback summary", async () => {
    useGlobal.mockReturnValue({ totalMark: 20, feedback: "" }); // Mock the useGlobal hook
    global.fetch = jest.fn().mockResolvedValueOnce({
      json: () => new Promise(() => {}), // Simulate a pending promise
    });
    const { getByText } = render(<Review />);
    expect(getByText("Feedback summary:")).toBeInTheDocument();
  });
});
