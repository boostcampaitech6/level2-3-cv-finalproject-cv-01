import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { ButtonAi } from "../../components/ButtonAi";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { Two } from "../../icons/Two";
import axios from 'axios';
import "./style.css";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart} from 'react-ts-tradingview-widgets';


export const ResultScreen = () => {
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
      navigate(`/result-2/${symbol}`, {
        state: { stockLabel: stockLabel, symbol: symbol}
      });
    }


  return (
    <div className="result-screen">
      <div className="frame-17">
        <div className="content-8">
          <div className="info-5">
            <div className="frame-18">
              <div className="text-wrapper-37">73,300</div>
            </div>
            <div className="frame-19">
              <div className="text-wrapper-37">+1,100 (1.52%)</div>
            </div>
            <div className="frame-20">
              <div className="text-wrapper-38">KOSPI 005930</div>
            </div>
            <div className="frame-21">
              <div className="text-wrapper-38">시가총액 489.80조</div>
            </div>
            <div className="frame-22">
              <div className="text-wrapper-38">시가총액 ㅇ위</div>
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
          
          <div className="button-AI-wrapper" onClick={handleButtonClick}>
            <ButtonAi className="button-AI-instance" />
          </div>
          <div className="menu-bar-4">
            <Menu
              className="menu-6"
              iconVariantsIconHome="/img/home-7.svg"
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
          <div className="head-6">
            <div className="stock-21">
              <div className="text-wrapper-39">{stockLabel}</div>
            </div>
            <div className="button-5">
              <Heart className="heart-4" stateProp="off" />
              <Two className="instance-1" color="#BEBEBE" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
