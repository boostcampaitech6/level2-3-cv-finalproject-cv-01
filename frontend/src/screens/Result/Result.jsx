import React, { useState, useEffect } from 'react';
import { Button } from "../../components/Button";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { Two } from "../../icons/Two";
import axios from 'axios';
import "./style.css";
import { useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart, SymbolInfo } from 'react-ts-tradingview-widgets';
import React, { useState, useEffect } from 'react';

import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import { ChartOptions } from 'chart.js';

import GaugeChart from 'react-gauge-chart'

// 차트 데이터
const scores = [1, 2, 3, 4, 5,6];

// 차트 옵션
const COLOR = {
  ORANGE_1: 'rgba(255, 108, 61, 1)',  
  GRAY_9E: 'rgba(158, 158, 158, 1)',  
  BLACK: '#000000'                    
};

export const Result = () => {
  // 애니메이션을 제어하기 위한 상태
  const [percent, setPercent] = useState(0.4);

  // 클릭 이벤트를 처리하는 함수
  const handleClick = () => {
    // 애니메이션을 재시작하기 위해 percent를 0으로 설정하고,
    // 바로 이어서 원래 값으로 되돌림
    setPercent(0);
    setTimeout(() => setPercent(0.6), 0);
  };


  // 차트 데이터
  const chartData = {
    labels: ['CNN', 'HMM', 'AR', 'News', ['Candle   ', 'Matching'], 'LSTM'],
    datasets: [
      {
        label: '팀 점수',
        data: scores,
        backgroundColor: 'rgba(255, 108, 61, 0.2)',
      },
    ],
  };

  // 차트 옵션
  const chartOptions = {
      elements: {
        //데이터 속성.
        line: {
          borderWidth: 2,
          borderColor: COLOR.ORANGE_1,
        },
        //데이터 꼭짓점.
        point: {
          pointBackgroundColor: COLOR.ORANGE_1,
        },
      },
      scales: {
        r: {
          ticks: {
            stepSize: 2.5,
            display: false,
          },
          grid: {
            color: COLOR.GRAY_9E,
          },
          //라벨 속성 지정.
          pointLabels: {
            font: {
              size: 16,
              weight: 'bold',
              family: "Noto Sans KR",
            },
            color: COLOR.BLACK,
          },
          angleLines: {
            display: false,
          },
          suggestedMin: 0,
          suggestedMax: 10,
        },
      },
      //위에 생기는 데이터 속성 label 타이틀을 지워줍니다.
      plugins: {
        legend: {
          display: false,
        },
      },
      //기본 값은 가운데에서 펴져나가는 애니메이션 형태입니다.
      animation: {
        duration: 0,
      },
      layout: {
        padding: {
          right: 30, // 왼쪽 여백을 20px로 설정
        },
      },
    
    };

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
        <div className="radar-chart-container">
          <div className='radar-chart-color'>
            <Radar data={chartData} options={chartOptions} />
            </div>
          </div>
          <div className="gauge-chart-container clickable-cursor" onClick={handleClick}>
            <GaugeChart id="gauge-chart3" 
              animate={true}
              hideText={true}
              nrOfLevels={5}
              cornerRadius={0}
              arcWidth={0.06}
              arcPadding={0.015}
              percent={0.6}
              textColor="#3C3C3C"
              needleColor="#7d49f5"
              needleBaseColor="#4616B5"
              colors={["#DF5341", "#782A2B", "#42464F", "#1F3A82","#3764F3" ]}
            />
            <div className="gauge-labels">
              <span className="gauge-label left">STRONG<br />SELL</span>
              <span className="gauge-label left2">SELL</span>
              <span className="gauge-label middle">NEUTRAL</span>
              <span className="gauge-label right2">BUY</span>
              <span className="gauge-label right">STRONG<br /> BUY</span>
            </div>
          </div>
          
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
