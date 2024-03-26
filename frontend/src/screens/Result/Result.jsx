import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { Button } from "../../components/Button";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { Two } from "../../icons/Two";
import axios from 'axios';
import "./style.css";
import { useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart, SymbolInfo } from 'react-ts-tradingview-widgets';
import React, { useState, useEffect } from 'react';


export const Result = () => {
  const { symbol } = useParams(); // URL 파라미터에서 symbol 값을 가져옵니다.
  const location = useLocation();
  const { stockLabel } = location.state || {};

  const [newsData, setNewsData] = useState([]);

  useEffect(() => {
    const fetchNewsData = async () => {
      try {
        console.log(stockLabel)
        const response = await axios.get(`http://localhost:8001/news/?query=${encodeURIComponent(stockLabel)}`);
        setNewsData(response.data);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    };

    fetchNewsData();
  }, []);

  return (
    <div className="result">
      <div className="frame-11">
        <div className="content-7">
          <div className="info-4">
            <SymbolInfo
              colorTheme="light"
              symbol={symbol}
              width="100%"
              isTransparent={true}
              marketCap
            />
          </div>
          <div className="chart-container">
            <AdvancedRealTimeChart 
              theme="light" 
              symbol={symbol}
              autosize={true}
              interval="D"
          />
          </div>

          <div className="news-container">
            {newsData.map((item, index) => (
              <div key={index} className="news-item">
                <a href={item.link} target="_blank" rel="noopener noreferrer" className="news-link">
                  <h2 className="news-title">{item.title.replace(/<b>|<\/b>/g, '')}</h2>
                  <p className="news-description">{item.description.replace(/<b>|<\/b>/g, '')}</p>
                </a>
              </div>
            ))}
          </div>
          
          <div className="button-wrapper">
            <Button className="button-instance" state="on" />
          </div>
          <div className="menu-bar-3">
            <Menu
              className="menu-5"
              iconVariantsIconHome="/img/home-8.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsIconUser="/img/user.svg"
              iconVariantsState="off"
              iconVariantsState1="off"
              iconVariantsState2="off"
              iconVariantsState3="off"
              to="/home"
              to1="/favorite"
              to2="/profile"
              to3="/search"
            />
          </div>
          <div className="head-5">
            <div className="stock-20">
              <div className="text-wrapper-36">{stockLabel}</div>
            </div>
            <div className="button-4">
              <Heart className="heart-2" stateProp="off" />
              <Two className="instance-2" color="#7D49F5" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
