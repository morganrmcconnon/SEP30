import { useState } from 'react';
import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  country_code: string,
  country_name: string,
  latitude: number | null,
  longitude: number | null,
};

const defaultResultData: ResultData = {
  country_code: '',
  country_name: '',
  latitude: null,
  longitude: null,
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
      <VisHeader title="Location detection" subtitle="Detect coordinates and country from location description" />
      <article className='text-black-white'>
        <form onSubmit={getResult}>
          <div>
            <input
              type="text"
              value={input.text}
              onChange={(e) => setInput({ ...input, text: e.target.value })}
              placeholder="User location description"
            />
          </div>
          <div>
            <button type="submit">Submit</button>
          </div>
          <div>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <p>Country name: {resultData.country_name === "" ? "Not found" : resultData.country_name}</p>
        <p>Country code: {resultData.country_code === "" ? "Not found" : resultData.country_code}</p>
        <p>Lattitude: {resultData.latitude === null ? 'Not found' : resultData.latitude}</p>
        <p>Longitude: {resultData.latitude === null ? 'Not found' : resultData.longitude}</p>
      </article>
    </div>

  );
};

export default DemoLocation;