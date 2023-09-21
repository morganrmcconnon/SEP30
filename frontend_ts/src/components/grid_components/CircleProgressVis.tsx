import React, { useLayoutEffect } from 'react';

export default function CircleProgressVis({ textColor, bgColor, percent }: { textColor: string, bgColor: string, percent: number }) {
  const [presentCircle, setPresentCircle] = React.useState(0);
  useLayoutEffect(() => {
    setPresentCircle(215 - (215 * percent) / 100);
  }, [percent]);
  return (
    <div className='CPpercent'>
      <svg>
        <circle cx={34} cy={34} r={34} />
        <circle cx={34} cy={34} r={34} style={{ stroke: bgColor, strokeDashoffset: presentCircle }} />
      </svg>
      <div className='CPnumber'>
        <h2 style={{ color: textColor }}>
          {percent}
          <span>%</span>
        </h2>
      </div>
    </div>
  );
}
