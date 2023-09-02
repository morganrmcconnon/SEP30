import React from 'react';
import VisHeader from '../VisHeader';
import { useCounter } from './CounterContext';

function Card() {
  const { count } = useCounter();

  return (
    <div className="vis-container">
      <VisHeader title="Result of Counter" subtitle="Bar Subtitle" />
      <p>Count: {count}</p>
      <p>Count * 2: {count * 2}</p>
    </div>
  );
}

export default Card;
