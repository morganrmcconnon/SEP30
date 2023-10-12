import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from "../../contexts/DashboardContext";


const TestEndpoint = () => {
  const [text, setText] = useState("");
  const { updateBackendData } = useSearchContext();

  const clearText = () => {
    setText("");
  };

  const setTextStatic = () => {
    setText("/backend/get_cached");
  };

  const getResult = (e : any) => {
    e.preventDefault();
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      // body: JSON.stringify({ 'text': text }),
    };
    console.log(`API endpoint sent: "${text}"`);
    fetch(text, requestOptions)
      .then((res) => res.json())
      .then((data) => {
        updateBackendData(data);
      })
      .catch((err) => {
        console.log(`Something went wrong with executing endpoint "${text}":`);
        console.log(err);
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Test API Endpoint" subtitle="Enter an API endpoint and check it's response in the Console." />
      <article>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter an api endpoint..."
            />
          </div>
          <div>
            <button type="submit">Console log endpoint's result</button>
          </div>
          <div>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
          <div>
            <button type="submit" onClick={setTextStatic}>Test Dashboard</button>
          </div>
          <div>
            {/* <p>{JSON.stringify(realData)}</p> */}
          </div>
        </form>
      </article>
    </div>

  );
};


export default TestEndpoint;