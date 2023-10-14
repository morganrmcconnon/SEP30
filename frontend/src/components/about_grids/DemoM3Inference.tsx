import { useState } from 'react';

import { Row, Col } from 'antd';

import VisHeader from '../grid_components/VisHeader';

type ResultData = {
  age_predicted: string | null,
  gender_predicted: string | null,
  org_predicted: string | null,
};


const defaultResultData: ResultData = {
  age_predicted: null,
  gender_predicted: null,
  org_predicted: null,
};

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
      <VisHeader title="m3inference" subtitle="Predict user's demographics from user's name, screen name, description, and language" />
      <article className='text-black-white about-card'>
        <form onSubmit={getResult}>
          <Row>
            <Col span={12}>
              <input
                type="text"
                value={input.name}
                onChange={(e) => setInput({ ...input, name: e.target.value })}
                placeholder="Name"
              />
            </Col>
            <Col span={12}>
              <input
                type="text"
                value={input.screen_name}
                onChange={(e) => setInput({ ...input, screen_name: e.target.value })}
                placeholder="Screen name (@handle)"
              />
            </Col>
          </Row>
          <Row>
            <Col span={12}>
              <input
                type="text"
                value={input.description}
                onChange={(e) => setInput({ ...input, description: e.target.value })}
                placeholder="User description"
              />
            </Col>
            <Col span={12}>
              <input
                type="text"
                value={input.lang}
                onChange={(e) => setInput({ ...input, lang: e.target.value })}
                placeholder="(Optional) Language"
              />
            </Col>
          </Row>
          <div>
            <button type="submit">Submit</button>
            <button type="button" onClick={clearText}>Clear</button>
          </div>
        </form>
        <div className='about-card-result'>
          <ul>
            <li>Age group: {resultData.age_predicted}</li>
            <li>Gender: {resultData.gender_predicted}</li>
            {resultData.org_predicted == 'non-org' ? <li>Is a person</li> : resultData.org_predicted == 'is-org' ? <li>Is an orgianization</li> : ""}
          </ul>
        </div>
      </article >
    </div >

  );
};

export default DemoM3Inference;