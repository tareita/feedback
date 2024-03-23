import React, { createContext, useContext, useState } from "react";

// Create a context to hold the global variable
const GlobalContext = createContext();

// Create a provider component to provide the global variable to all components
export const GlobalProvider = ({ children }) => {
  const [totalMark, setTotalMark] = useState(0); // Set your initial value here
  const [feedback, setFeedback] = useState("");
  return (
    <GlobalContext.Provider
      value={{ totalMark, setTotalMark, feedback, setFeedback }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

// Custom hook to easily access the global variable from any component
export const useGlobal = () => useContext(GlobalContext);
