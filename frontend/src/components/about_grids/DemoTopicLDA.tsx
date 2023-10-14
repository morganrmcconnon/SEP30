import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  related_topics: {
    cosine_similarity: string[] | null,
    hellinger_distance: string[] | null,
  }
};

const defaultResultData: ResultData = {
  related_topics: {
    cosine_similarity: null,
    hellinger_distance: null,
  }
};

const DemoTopicLDA = () => {
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
      <VisHeader title="Topic modelling with LDA" subtitle="Topic Modelling and Inference using Latent Dirichlet Allocation" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter text..."
            />
          </div>
          <div className='about-card-buttons'>
            <button type="submit">Predict related topics</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <div className='about-card-result'>
          {
            resultData.related_topics.cosine_similarity === null ? '' :
              resultData.related_topics.cosine_similarity.length === 0 ? <p>Unsure related topics</p> :
                <p>Related topics: {
                  resultData.related_topics.cosine_similarity.map((topic) => <li>{topic}</li>)
                }
                </p>
          }
        </div>
      </article>
    </div>

  );
};

export default DemoTopicLDA;