import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const DemoSentimentVader = () => {
  const [text, setText] = useState("");
  const [resultData, setResultData] = useState({
    sentiment_result: '',
    compound_score: '',
  });

  const clearText = () => {
    setText("");
    setResultData({
      sentiment_result: '',
      compound_score: '',
    });
  };

  const getResult = (e : any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/sentiment/vader", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        setResultData({
          sentiment_result: data['sentiment_label'],
          compound_score: data['compound_score'],
        });
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/sentiment/vader!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Sentiment Analysis" subtitle="Sentiment Analysis with NLTK Vader sentiment model" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter a sentence..."
            />
          </div>
          <div className='about-card-buttons'>
            <button type="submit">Check sentiment</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <p>Result: {resultData['sentiment_result']}</p>
        <p>Compound Score: {resultData['compound_score']}</p>
      </article>
    </div>

  );
};

export default DemoSentimentVader;