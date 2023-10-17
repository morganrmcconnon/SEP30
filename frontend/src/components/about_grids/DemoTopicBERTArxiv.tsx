import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  probability: number | null,
  topic_id: number | null,
  topic_name: string | null,
};

const defaultResultData: ResultData = {
  probability: null,
  topic_id: null,
  topic_name: null,
};


const DemoTopicBERTArxiv = () => {
  const [text, setText] = useState("");
  const [resultData, setResultData] = useState(defaultResultData);

  const clearText = () => {
    setText("");
    setResultData(defaultResultData);
  };

  const getResult = (e: any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/topic/bertaxiv", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/topic/bertaxiv!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/topic/bertaxiv!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="BERTArxiv topic model" subtitle="Predict a text's topic with BERTArxiv topic model" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter text..."
            />
          </div>
          <div className='about-card-buttons'>
            <button type="submit">Predict the text's topic</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <div className='about-card-result'>
          <ul>
            <li>Topic id: {resultData.topic_id}</li>
            <li>Topic name: {resultData.topic_name}</li>
            <li>Mental Health related (ID = 55?): {(resultData.topic_id === 55) ? 'Yes' : (resultData.topic_id !== null) ? 'No' : ''}</li>
          </ul>
        </div>
      </article>
    </div>

  );
};

export default DemoTopicBERTArxiv;