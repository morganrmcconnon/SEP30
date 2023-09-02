import React from 'react';
import VisHeader from "../VisHeader";
import { useCounter } from './CounterContext';

function CounterCard() {
  const { count, increment, decrement } = useCounter();

  return (
    <div className="vis-container">
      <VisHeader title="Counter" subtitle="Bar Subtitle" />
      <p>Counter: {count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  );
}

export default CounterCard;
