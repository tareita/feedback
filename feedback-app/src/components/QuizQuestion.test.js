import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react";
import QuizQuestion from "./QuizQuestion";
import { API_URL } from "../config";
import { useGlobal } from "../contexts/Context";
import * as ContextModule from "../contexts/Context";

// Mock the useGlobal hook
jest.mock("../contexts/Context", () => ({
  useGlobal: () => ({
    setTotalMark: jest.fn(), // Provide a mock function for setTotalMark
    feedback: "", // Provide dummy value for feedback
    setFeedback: jest.fn(), // Provide a mock function for setFeedback
  }),
}));

describe("QuizQuestion component", () => {
  test("renders question correctly", () => {
    const questionText =
      "List the three main security properties and briefly describe the purpose of each one.";
    const { getByText } = render(
      <QuizQuestion
        question={questionText}
        questionNumber={1}
        marks={6}
        showCorrectAnswer={false}
      />
    );

    expect(getByText(questionText)).toBeInTheDocument();
  });

  test("updates answer state on change", () => {
    const mockOnAnswerChange = jest.fn();
    const { getByPlaceholderText } = render(
      <QuizQuestion
        question="List the three main security properties and briefly describe the purpose of each one."
        questionNumber={1}
        marks={6}
        showCorrectAnswer={false}
        onAnswerChange={mockOnAnswerChange}
      />
    );
    const answerInput = getByPlaceholderText("Your answer");

    fireEvent.change(answerInput, { target: { value: "Paris" } });

    expect(answerInput).toHaveValue("Paris");
  });

  test("fetches feedback when showCorrectAnswer changes", async () => {
    const mockSetLoading = jest.fn();
    const mockSetCorrectAnswer = jest.fn();
    const mockSetQuestionMark = jest.fn();
    const mockSetCurrFeedback = jest.fn();
    const mockUseGlobal = jest.fn();
    mockUseGlobal.mockReturnValue({
      setTotalMark: jest.fn(),
      setFeedback: jest.fn(),
      feedback: "",
    });

    jest.spyOn(ContextModule, "useGlobal").mockImplementation(mockUseGlobal);

    global.fetch = jest.fn().mockResolvedValueOnce({
      json: () => Promise.resolve({ answer: "Paris" }),
    });

    const { rerender } = render(
      <QuizQuestion
        question="List the three main security properties and briefly describe the purpose of each one."
        questionNumber={1}
        marks={10}
        showCorrectAnswer={false}
        setLoading={mockSetLoading}
        setCorrectAnswer={mockSetCorrectAnswer}
        setQuestionMark={mockSetQuestionMark}
        setCurrFeedback={mockSetCurrFeedback}
      />
    );

    rerender(
      <QuizQuestion
        question="List the three main security properties and briefly describe the purpose of each one."
        questionNumber={1}
        marks={10}
        showCorrectAnswer={true}
        setLoading={mockSetLoading}
        setCorrectAnswer={mockSetCorrectAnswer}
        setQuestionMark={mockSetQuestionMark}
        setCurrFeedback={mockSetCurrFeedback}
      />
    );

    expect(global.fetch).toHaveBeenCalledWith(API_URL + "api/v1/chat", {
      method: "POST",
      body: JSON.stringify({
        prompt:
          "Question:List the three main security properties and briefly describe the purpose of each one. Answer: Marks:10",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  });
});
