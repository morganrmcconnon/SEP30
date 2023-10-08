import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const DemoTopicCardiffNLP = () => {
  const [text, setText] = useState("");
  const [resultData, setResultData] = useState({});

  const clearText = () => {
    setText("");
    setResultData({});
  };

  const getResult = (e: any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/topic/cardiffnlp", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/topic/cardiffnlp!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/topic/cardiffnlp!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Topic inference" subtitle="Detect topic of a text with CardiffNLP's Tweet Topic RoBERTa Model" />
      <article className='text-black-white'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter a sentence..."
            />
          </div>
          <div>
            <button type="submit">Check topic</button>
          </div>
          <div>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <p>{JSON.stringify(resultData)}</p>
      </article>
    </div>

  );
};

export default DemoTopicCardiffNLP;