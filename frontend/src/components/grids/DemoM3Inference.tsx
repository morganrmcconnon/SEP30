import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const defaultResultData = {};

const DemoM3Inference = () => {

  const [input, setInput] = useState({
    name: "",
    screen_name: "",
    description: "",
    lang: "",
  });
  const [resultData, setResultData] = useState(defaultResultData);

  const clearText = () => {
    setInput({
      name: "",
      screen_name: "",
      description: "",
      lang: "",
    });
    setResultData(defaultResultData);
  };

  const getResult = (e: any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    };
    fetch("/api/analysis/user/demographics/m3inference", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/user/demographics/m3inference!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/user/demographics/m3inference!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Detect demographics with m3inference" subtitle="Detect user's demographics with m3inference from user's name, screen name, description, and language" />
      <article className='text-black-white'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={input.name}
              onChange={(e) => setInput({ ...input, name: e.target.value })}
              placeholder="Name"
            />
            <input
              type="text"
              value={input.screen_name}
              onChange={(e) => setInput({ ...input, screen_name: e.target.value })}
              placeholder="Screen name"
            />
            <input
              type="text"
              value={input.description}
              onChange={(e) => setInput({ ...input, description: e.target.value })}
              placeholder="Description"
            />
            <input
              type="text"
              value={input.lang}
              onChange={(e) => setInput({ ...input, lang: e.target.value })}
              placeholder="Language"
            />
          </div>
          <div>
            <button type="submit">Submit</button>
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

export default DemoM3Inference;