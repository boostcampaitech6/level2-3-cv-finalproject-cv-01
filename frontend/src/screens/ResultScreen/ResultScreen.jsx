import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { ButtonAi } from "../../components/ButtonAi";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { Two } from "../../icons/Two";
import axios from 'axios';
import "./style.css";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart, SymbolInfo} from 'react-ts-tradingview-widgets';
import { Radar } from 'react-chartjs-2';
import GaugeChart from 'react-gauge-chart'

// 차트 데이터
const scores = [1, 2, 3, 4, 5, 6];

// 차트 옵션
const COLOR = {
  ORANGE_1: 'rgba(255, 108, 61, 1)',  
  GRAY_9E: 'rgba(158, 158, 158, 1)',  
  BLACK: '#000000'                    
};

export const ResultScreen = () => {
  const navigate = useNavigate();

  const { symbol } = useParams(); // URL 파라미터에서 symbol 값을 가져옵니다.
  const location = useLocation();
  const { stockLabel } = location.state || {};

  const [newsData, setNewsData] = useState([]);
  const [showAdditionalResults, setShowAdditionalResults] = useState(false);

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

  useEffect(() => {
    const fetchNewsData = async () => {
      try {
        console.log(stockLabel)
        const response = await axios.get(`http://${process.env.SERVER_IP}:8001/news/?query=${encodeURIComponent(stockLabel)}`);
        setNewsData(response.data);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    };

    fetchNewsData();
  }, []);

  const handleButtonClick = () => {
    setShowAdditionalResults(true); // ButtonAi 클릭 시 추가 결과를 보여줄 상태로 변경
  };

    const [likes, setLikes] = useState({}); // 각 주식의 '좋아요' 상태를 관리합니다.

    const toggleLike = (symbol) => {
      setLikes((currentLikes) => ({
        ...currentLikes,
        [symbol]: !currentLikes[symbol], // 토글된 상태를 저장합니다.
      }));
    };


  return (
    <div className="result-screen">
      <div className="frame-17">
        <div className="content-8">
          <div className="info-5">
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

            {showAdditionalResults && (
            <div className="additional-results-container">
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
            </div>
          )}
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
              <Heart 
                className="heart-4" 
                stateProp={likes ? "on" : "off"}
                onHeartClick={() => toggleLike({symbol})}
              />
              <Two className="instance-1" color="#BEBEBE" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
