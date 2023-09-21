import React from "react";
import { Col, Divider, Row } from "antd";
import { BsCheck2 } from "react-icons/bs";

import VisHeader from "../grid_components/VisHeader";
import ProgressBar from "../grid_components/ProgressBar";
import DATATYPES from "../../constants/dataTypes";
import { useSearchContext } from "../../contexts/SearchContext";

export default function GendersGrid() {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const data = dashboardData.genders;
  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <div style={{ padding: 20 }}>
          <Row>
            <Col span={4} style={{ display: "flex", alignItems: "center" }}>
              <p style={{ fontSize: 16 }}>Female:</p>
            </Col>
            <Col span={20}>
              <ProgressBar
                width="100%"
                height={30}
                rounded={3}
                percent={data?.data.female.present}
                color={data?.data.female.color}
              />
            </Col>
          </Row>
          <Row style={{ marginTop: 20 }}>
            {Object.keys(data?.data.female.sentiment).map((item, index) => (
              <Col span={12} style={{ marginTop: 5 }} key={index}>
                <div style={{ display: "flex" }}>
                  <BsCheck2
                    color="#39b54a"
                    size={20}
                    style={{ marginRight: 10 }}
                  />
                  <p style={{ textTransform: "capitalize" }}>
                    {item} {data?.data.female.sentiment[item]}
                  </p>
                </div>
              </Col>
            ))}
          </Row>
          <Divider />
          <Row>
            <Col span={4} style={{ display: "flex", alignItems: "center" }}>
              <p style={{ fontSize: 16 }}>Male:</p>
            </Col>
            <Col span={20}>
              <ProgressBar
                width="100%"
                height={30}
                rounded={3}
                percent={data?.data.male.present}
                color={data?.data.male.color}
              />
            </Col>
          </Row>
          <Row style={{ marginTop: 20 }}>
            {Object.keys(data?.data.male.sentiment).map((item, index) => (
              <Col span={12} style={{ marginTop: 5 }} key={index}>
                <div style={{ display: "flex" }}>
                  <BsCheck2
                    color="#39b54a"
                    size={20}
                    style={{ marginRight: 10 }}
                  />
                  <p style={{ textTransform: "capitalize" }}>
                    {item} {data?.data.male.sentiment[item]}
                  </p>
                </div>
              </Col>
            ))}
          </Row>
        </div>
      </div>
    </div>
  );
}
