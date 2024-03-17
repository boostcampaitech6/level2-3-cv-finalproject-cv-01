import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { Heart } from "../../components/Heart";
import { Loding } from "../../components/Loding";
import { Menu } from "../../components/Menu";
import { Two } from "../../icons/Two";
import axios from 'axios';
import "./style.css";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart} from 'react-ts-tradingview-widgets';
import { SyncLoader } from "react-spinners";


export const ResultWrapper = () => {
  const navigate = useNavigate();
  
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

  const handleButtonClick = () => {
    navigate(`/result-3/${symbol}`, {
      state: { stockLabel: stockLabel, symbol: symbol}
    });
  }

  return (
    <div className="result-wrapper">
      <div className="frame-23" to="/result-3">
        <div className="content-9">
          <div className="info-6">
            <div className="frame-24">
              <div className="text-wrapper-40">73,300</div>
            </div>
            <div className="frame-25">
              <div className="text-wrapper-40">+1,100 (1.52%)</div>
            </div>
            <div className="frame-26">
              <div className="text-wrapper-41">KOSPI 005930</div>
            </div>
            <div className="frame-27">
              <div className="text-wrapper-41">시가총액 489.80조</div>
            </div>
            <div className="frame-28">
              <div className="text-wrapper-41">시가총액 ㅇ위</div>
            </div>
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

          <div className="loding-wrapper" onClick={handleButtonClick}>
            <SyncLoader color="#7d49f5" />
          </div>
          <div className="menu-bar-5">
            <Menu
              className="menu-7"
              iconVariantsIconHome="/img/home-7.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsIconUser="/img/user.svg"
              iconVariantsState="off"
              iconVariantsState1="off"
              iconVariantsState2="off"
              iconVariantsState3="off"
            />
          </div>
          <div className="head-7">
            <div className="stock-22">
              <div className="text-wrapper-42">{stockLabel}</div>
            </div>
            <div className="button-6">
              <Heart className="heart-5" stateProp="off" />
              <Two className="instance-2-instance" color="#BEBEBE" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
