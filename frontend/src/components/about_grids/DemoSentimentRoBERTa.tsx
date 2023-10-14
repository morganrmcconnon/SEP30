import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const DemoSentimentRoBERTa = () => {
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

  const getResult = (e: any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/sentiment/roberta", requestOptions)
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
          // Capitalise first letter of sentiment_result
          sentiment_result: sentiment_result.charAt(0).toUpperCase() + sentiment_result.slice(1),
          negative: negative_percent.toString() + "%",
          neutral: neutral_percent.toString() + "%",
          positive: positive_percent.toString() + "%",
        });
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/sentiment/roberta!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="RoBERTa Sentiment model" subtitle="Sentiment analysis with CardiffNLP's Twitter RoBERTa Sentiment" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text..."
          />
          <div className='about-card-buttons'>
            <button type="submit">Predict sentiment</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <div className='about-card-result'>
          <p>Result: {resultData['sentiment_result']}</p>
          <p>Probability of the text sentiment being:</p>
          <ul>
            <li>Positive: {resultData['positive']}</li>
            <li>Neutral: {resultData['neutral']}</li>
            <li>Negative: {resultData['negative']}</li>
          </ul>
        </div>
      </article >
    </div >

  );
};

export default DemoSentimentRoBERTa;