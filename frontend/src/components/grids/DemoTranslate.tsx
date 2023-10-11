import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const defaultResultData = {
  'in_english': '',
  'lang_detected': '',
};

const DemoTranslate = () => {
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
    fetch("/api/analysis/translate", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/translate!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/translate!");
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
        <p>{JSON.stringify(resultData)}</p>
        <p>In English: {resultData['in_english']}</p>
        <p>Language detected: {resultData['lang_detected']}</p>
      </article>
    </div>

  );
};

export default DemoTranslate;