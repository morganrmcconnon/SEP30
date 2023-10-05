import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const DemoTranslate = () => {
  const [text, setText] = useState("");
  const [resultData, setResultData] = useState({
    sentiment_result: '',
    negative: '',
    neutral: '',
    positive: '',
  });

  const clearText = () => {
    setText("");
    setResultData({
      sentiment_result: '',
      negative: '',
      neutral: '',
      positive: '',
    });
  };

  const getResult = (e : any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/translate", requestOptions)
      .then((res) => res.json())
      .then((data) => {

        const negative = data['confidence_probabilities']['negative'];
        const neutral = data['confidence_probabilities']['neutral'];
        const positive = data['confidence_probabilities']['positive'];
        const sentiment_result = data['sentiment_result'];

        // convert to percentages, round to nearest 2 decimal places
        const negative_percent = Math.round(negative * 10000) / 100;
        const neutral_percent = Math.round(neutral * 10000) / 100;
        const positive_percent = Math.round(positive * 10000) / 100;

        setResultData({
          sentiment_result: sentiment_result,
          negative: negative_percent.toString() + "%",
          neutral: neutral_percent.toString() + "%",
          positive: positive_percent.toString() + "%",
        });
      })
      .catch((err) => {
        console.log("Something went wrong NASA!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Translate text" subtitle="Translate text with Google Translate" />
      <article className='text-black-white'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter a text to translate..."
            />
          </div>
          <div>
            <button type="submit">Translate</button>
          </div>
          <div>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <p>Result: {resultData['sentiment_result']}</p>
        <p>Negative: {resultData['negative']}</p>
        <p>Neutral: {resultData['neutral']}</p>
        <p>Positive: {resultData['positive']}</p>
      </article>
    </div>

  );
};

export default DemoTranslate;