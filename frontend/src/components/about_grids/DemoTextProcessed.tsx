import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  text_processed: string[] | null,
};

const defaultResultData: ResultData = {
  text_processed: null,
};

const DemoTextProcessed = () => {
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
    fetch("/api/analysis/text/processed", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/text/processed!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/text/processed!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Process sentence" subtitle="Tokenize sentence, lemmatize words, and remove stop words." />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter sentence..."
            />
          </div>
          <div className='about-card-buttons'>
            <button type="submit">Submit</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        {
          resultData.text_processed === null ? (<p>Enter a sentence to process.</p>) :
            (resultData.text_processed === undefined || resultData.text_processed.length === 0) ? (<p>[No words]</p>) : (
              <>
                <p>Words:</p>
                <p>{resultData.text_processed.join(', ')}</p>
              </>
            )
        }
      </article>
    </div>

  );
};

export default DemoTextProcessed;