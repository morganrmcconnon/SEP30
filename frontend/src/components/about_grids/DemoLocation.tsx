import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  country_code: string | undefined,
  country_name: string | undefined,
  latitude: number | null | undefined,
  longitude: number | null | undefined,
};

const defaultResultData: ResultData = {
  country_code: undefined,
  country_name: undefined,
  latitude: undefined,
  longitude: undefined,
};

const DemoLocation = () => {
  const [input, setInput] = useState({
    text: "",
  });
  const [resultData, setResultData] = useState(defaultResultData);

  const clearText = () => {
    setInput({
      text: "",
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
    fetch("/api/analysis/user/location", requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log("Success /api/analysis/user/location!");
        setResultData(data);
      })
      .catch((err) => {
        console.log("Something went wrong /api/analysis/user/location!");
        console.error(err);
      });
  };

  return (
    <div className="vis-container">
      <VisHeader title="Location analysis" subtitle="Predict coordinates and country from location description" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={input.text}
              onChange={(e) => setInput({ ...input, text: e.target.value })}
              placeholder="User's location description"
            />
          </div>
          <div className='about-card-buttons'>
            <button type="submit">Submit</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <div className='about-card-result'>
          {
            resultData.country_name === undefined && resultData.country_code === undefined && resultData.latitude === undefined && resultData.longitude === undefined ? (<p>Enter a user's location description to predict.</p>) : (
              <ul>
                <li>Country name: {resultData.country_name === "" ? "Not found" : resultData.country_name}</li>
                <li>Country code: {resultData.country_code === "" ? "Not found" : resultData.country_code}</li>
                <li>Lattitude: {resultData.latitude === null ? 'Not found' : resultData.latitude}</li>
                <li>Longitude: {resultData.latitude === null ? 'Not found' : resultData.longitude}</li>
              </ul>
            )
          }
        </div>
      </article>
    </div>

  );
};

export default DemoLocation;