import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  is_related: boolean | null,
};

const defaultResultData: ResultData = {
  is_related: null,
};

const DemoFilterTweetsSpacy = () => {
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
    fetch("/api/analysis/filter/spacy", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/filter/spacy!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/filter/spacy!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Filter tweets" subtitle="Detect if a tweet is not spam and mental health related using spacy" />
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
            <button type="submit">Submit</button>
          </div>
          <div>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <p>Text is related to mental health: {
          resultData.is_related === null ? '' :
            resultData.is_related === true ? 'True' : 'False'
        }</p>
      </article>
    </div>

  );
};

export default DemoFilterTweetsSpacy;