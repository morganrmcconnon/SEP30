import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

const defaultResultData = {};

const DemoTopicLDA = () => {
  const [text, setText] = useState("");
  const [resultData, setResultData] = useState(defaultResultData);

  const clearText = () => {
    setText("");
    setResultData(defaultResultData);
  };

  const getResult = (e : any) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'text': text }),
    };
    fetch("/api/analysis/topic/lda", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/topic/lda!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/topic/lda!");
        console.error(err);
      });
  };


  return (
    <div className="vis-container">
      <VisHeader title="Topic modelling" subtitle="Topic Modelling and Inference using Latent Dirichlet Allocation" />
      <article className='text-black-white'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter a tweet related to mental health to get its topics."
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

export default DemoTopicLDA;