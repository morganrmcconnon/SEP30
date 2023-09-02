import { createContext, useContext, useState } from 'react';

// Create a context
const CounterContext = createContext(0);

// Create a provider component to manage the state
export function CounterProvider({ children }) {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(count + 1);
  };

  const decrement = () => {
    if (count > 0) {
      setCount(count - 1);
    }
  };

  return (
    <CounterContext.Provider value={{ count, increment, decrement }}>
      {children}
    </CounterContext.Provider>
  );
}

// Custom hook to access the counter context
export function useCounter() {
  return useContext(CounterContext);
}
