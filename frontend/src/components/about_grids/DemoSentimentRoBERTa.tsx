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
          sentiment_result: sentiment_result,
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
      <article className='text-black-white' style={
        {
          marginTop: '0.5em', marginLeft: '1em', marginRight: '1em', marginBottom: '0.5em', 
        }
      }>
        <form onSubmit={getResult}>
          <input
            type="text"
            style={
              // make input text box in the middle, almost full width
              {
                marginRight: '1em', marginBottom: '0.5em',
                width: '90%',
                display: 'block',
                padding: '10px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                boxSizing: 'border-box',
              }
            }
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter a sentence to check it's sentiment"
          />
          <div style={{
            marginRight: '1em', marginBottom: '0.5em',
          }}>
            <button type="submit"
              style={
                // Make button style consistent with input text box
                {
                  marginRight: '0.5em',
                  padding: '10px',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                }
              }
            >Check sentiment</button>
            <button type="button" onClick={clearText} style={
              // Make button style consistent with input text box
              {
                padding: '10px',
                border: '1px solid #ccc',
                borderRadius: '4px',
              }
            }>Clear</button>
          </div>

        </form>
        <div>
          <p style={{marginRight: '1em', marginBottom: '0.5em',}}>Result: {resultData['sentiment_result']}</p>
          <p>Probability of the text sentiment being:
            <ul style={{marginTop: '0.5em', marginBottom: '0.5em', paddingInlineStart: '1em'}}>
              <li>Positive: {resultData['positive']}</li>
              <li>Neutral: {resultData['neutral']}</li>
              <li>Negative: {resultData['negative']}</li>
            </ul>
          </p>
        </div>
      </article >
    </div >

  );
};

export default DemoSentimentRoBERTa;