import React from 'react';

export default function ProgressBar({ width, height, color, percent, rounded }) {
  return (
    <div style={{ width, height, backgroundColor: '#f3f3f4', borderRadius: rounded, overflow: 'hidden' }}>
      <div
        className='progress__bar'
        style={{ width: `${percent}%`, height: '100%', backgroundColor: color, borderRadius: rounded }}
      ></div>
    </div>
  );
}
