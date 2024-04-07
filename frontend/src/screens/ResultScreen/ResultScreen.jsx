import React, { useState, useEffect, useRef } from 'react';
import { ButtonAi } from "../../components/ButtonAi";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import axios from 'axios';
import "./style.css";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart, SymbolInfo} from 'react-ts-tradingview-widgets';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, defaults} from 'chart.js';
import 'chart.js/auto';
import GaugeChart from 'react-gauge-chart'
import { useUser } from '../../components/UserContext';
import { SyncLoader } from "react-spinners";
// 차트 옵션
const COLOR = {
  ORANGE_1: 'rgba(255, 108, 61, 1)',  
  GRAY_9E: 'rgba(158, 158, 158, 1)',  
  BLACK: '#000000'                    
};



export const ResultScreen = () => {

  
  const chartSectionRef = useRef(null);

  // 애니메이션과 버튼 표시 상태를 관리하기 위한 상태 변수
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [showButton, setShowButton] = useState(true); // 버튼이 초기에 보이게 설정

  const navigate = useNavigate();
  const { userInfo } = useUser();
  const { symbol } = useParams(); // URL 파라미터에서 symbol 값을 가져옵니다.
  const location = useLocation();
  const { stockLabel } = location.state || {};

  const [newsData, setNewsData] = useState([]);
  const [showAdditionalResults, setShowAdditionalResults] = useState(false); // 추가 결과가 초기에 숨겨지게 설정

  // 애니메이션을 제어하기 위한 상태
  const [percent, setPercent] = useState(0.4);

  const [marketTrend, setMarketTrend] = useState('');

  // 클릭 이벤트를 처리하는 함수
  const handleClick = () => {
    // 애니메이션을 재시작하기 위해 percent를 0으로 설정하고,
    // 바로 이어서 원래 값으로 되돌림
    setPercent(0);
    setTimeout(() => setPercent(0.6), 0);
  };

  // 차트 옵션
  const chartOptions = {
      elements: {
        //데이터 속성.
        line: {
          borderWidth: 2,
          borderColor: '#71985e',
        },
        //데이터 꼭짓점.
        point: {
          pointBackgroundColor: '#71985e',
        },
      },
      scales: {
        r: {
          ticks: {
            stepSize: 20,
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
            color: '#ffffff',
            padding: 20,
          },
          angleLines: {
            display: false,
          },
          suggestedMin: 0,
          suggestedMax: 100,
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
    
    };

  const [CNNData, setCNNData] = useState([]);
  const [LSTMData, setLSTMData] = useState([]);
  const [ARData, setARData] = useState([]);
  const [HMMData, setHMMData] = useState([]);
  const [BertData, setBERTData] = useState([]);
  const [CandleData, setCANDLEData] = useState([]);

  

  useEffect(() => {
    const fetchNewsData = async () => {
      try {
        console.log(stockLabel)
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/news?query=${encodeURIComponent(stockLabel)}`);
        setNewsData(response.data);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    };

    fetchNewsData();

    const fetchCANDLEData = async () => {
      try {
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/candle?stock_code=${encodeURIComponent(formattedStockCode)}`);
        setCANDLEData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchCANDLEData();

    const fetchBERTData = async () => {
      try {
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/bert?stock_code=${encodeURIComponent(formattedStockCode)}`);
        setBERTData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchBERTData();

    const fetchCNNData = async () => {
      try {
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/cnn?stock_code=${encodeURIComponent(formattedStockCode)}`);
        setCNNData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchCNNData();


    const fetchLSTMData = async () => {
      try {
        // 모델 이름을 'lstm'으로 설정합니다.
        const model = 'lstm';
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/timeseries?model=${encodeURIComponent(model)}&stock_code=${encodeURIComponent(formattedStockCode)}`);
        setLSTMData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchLSTMData();

    const fetchARData = async () => {
      try {
        // 모델 이름을 'ar'으로 설정합니다.
        const model = 'ar';
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/timeseries?model=${encodeURIComponent(model)}&stock_code=${encodeURIComponent(formattedStockCode)}`);
        setARData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchARData();

    const fetchHMMData = async () => {
      try {
        // 모델 이름을 'hmm'으로 설정합니다.
        const model = 'hmm';
        const formattedStockCode = symbol.slice(-6);
        const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/pred/timeseries?model=${encodeURIComponent(model)}&stock_code=${encodeURIComponent(formattedStockCode)}`);
        setHMMData(response.data); // 상태 업데이트
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching time series data:", error);
      }
    };

    fetchHMMData();

  }, [stockLabel, symbol]);

  useEffect(() => {
    if (showAdditionalResults && chartSectionRef.current) {
      chartSectionRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [showAdditionalResults]);


  const handleButtonClick = () => {
    setIsAnalyzing(true); // 애니메이션 시작
    setShowButton(false); // 버튼 즉시 숨기기
  
    setTimeout(() => {
      setShowAdditionalResults(true); // 추가 결과 표시
      // 스크롤 기능 추가
      if (chartSectionRef.current) {
        chartSectionRef.current.scrollIntoView({ behavior: 'smooth' });
      }
      setIsAnalyzing(false); // 애니메이션 종료
    }, 3000); // 3초 후 실행
  };
  const [likes, setLikes] = useState({}); // 각 주식의 '좋아요' 상태를 관리합니다.

  // 사용자의 좋아요 상태를 로드하는 함수
  const loadLikes = async () => {
    try {
      const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/user/favorite/${userInfo.kakao_id}`);
      const fetchedLikes = response.data; // 서버 응답 구조에 맞게 조정
      // fetchedLikes가 좋아요한 주식의 배열이라고 가정하고, 이를 객체로 변환
      const likesUpdate = fetchedLikes.reduce((acc, cur) => ({
        ...acc,
        [cur.stock_code]: true // 여기서 cur.stock_code는 좋아요한 주식의 심볼을 나타냅니다.
      }), {});
      setLikes(likesUpdate);
    } catch (error) {
      console.error("Error loading favorites:", error);
    }
  };

  // 컴포넌트가 마운트될 때 사용자의 좋아요 상태를 로드
  useEffect(() => {
    loadLikes();
  }, []); // 빈 의존성 배열을 전달하여 컴포넌트가 마운트될 때만 실행되도록 함

  const toggleLike = async (symbol) => {
    const isLiked = !!likes[symbol]; // 현재 상태 확인
    console.log(`Current like status for ${symbol}:`, isLiked); // 현재 좋아요 상태 로깅
  
    const requestBody = {
      stock_code: symbol,
      like: !isLiked
    };
    console.log(`Sending request for ${symbol} with body:`, requestBody); // 전송되는 요청 본문 로깅
  
    try {
      const response = await axios.post(`http://${process.env.SERVER_IP}:${process.env.PORT}/user/favorite/${userInfo.kakao_id}`, requestBody);
      console.log(`Response for ${symbol}:`, response); // 요청에 대한 응답 로깅
  
      // 상태 업데이트
      setLikes({
        ...likes,
        [symbol]: !isLiked
      });
    } catch (error) {
      console.error(`Error updating favorite for ${symbol}:`, error); // 오류 로깅
    }
  };
  

  const [chartScores, setChartScores] = useState([]);

  useEffect(() => {
    // 모든 모델의 score 값 추출
    const scores = [
      CNNData.length > 0 ? CNNData[0].score : null,
      HMMData.length > 0 ? HMMData[0].score : null,
      ARData.length > 0 ? ARData[0].score : null,
      BertData.length > 0 ? BertData[0].score : null,
      CandleData.length > 0 ? CandleData[0].score : null,
      LSTMData.length > 0 ? LSTMData[0].score : null,
    ].filter(score => score != null);
  
    // 차트 데이터 업데이트
    if (scores.length > 0) {
      setChartScores(scores);
    }
  }, [CNNData, HMMData, ARData, BertData, CandleData, LSTMData]);
  
  const averageScorePercent = chartScores.length > 0
    ? chartScores.reduce((acc, curr) => acc + curr, 0) / chartScores.length / 100
    : 0; // 모델 점수가 없는 경우 0으로 설정

  // 차트 데이터
  const chartData = {
    labels: ['CNN', 'HMM', 'AR', 'BERT', 'CANDLE', 'LSTM'],
    datasets: [
      {
        label: 'Model Score',
        data: chartScores,
        backgroundColor: 'rgba(121, 151, 100, 0.2)',
      },
    ],
  };

  const [selectedImage, setSelectedImage] = useState('');

  useEffect(() => {
    let imagePath;
    if (averageScorePercent >= 0.55) {
      imagePath = 'positive';
    } else if (averageScorePercent >= 0.45) {
      imagePath = 'neutral';
    } else {
      imagePath = 'negative';
    }

    const imageIndex = Math.floor(Math.random() * 50);
    const imageUrl = `/result/${imagePath}/${imageIndex}.png`;
    
    setSelectedImage(imageUrl);
  }, [averageScorePercent]);

  const score = averageScorePercent * 100;

  useEffect(() => {
    let newMessage = '';
    
    if (score >= 80) {
      newMessage = '이건 못참지 🤪';
    } else if (score >= 60) {
      newMessage = '못먹어도 GO! 추매각 🤩';
    } else if (score >= 40) {
      newMessage = '좀 지켜봐야겠는데? 🤔';
    } else if (score >= 20) {
      newMessage = '좀 더 내려가고 나면 삽시다 😒';
    } else {
      newMessage = '어디까지 내려가는거에요 🥹';
    }

    setMessage(newMessage);
  }, [averageScorePercent]);


  useEffect(() => {
    if (score < 40) {
      setMarketTrend('하락세');
    } else if (score >= 40 && score <= 60) {
      setMarketTrend('보합세');
    } else if (score > 60) {
      setMarketTrend('상승세');
    }
  }, [score]);

  const [message, setMessage] = useState('');

  return (
    <div className="result-screen">
      <div className="design-frame">
        <div className="header">
            <div className="stock-21">
              <div className="text-wrapper-39">{stockLabel}</div>
            </div>
            <div className="button-5">
              <Heart 
                stateProp={likes[symbol] ? "on" : "off"} 
                onClick={() => toggleLike(symbol)}
              />
            </div>
          </div>
          {showButton && (
          <div className="button-AI-wrapper" onClick={handleButtonClick} >
              <ButtonAi className="button-AI-instance" />
            </div>
             )}
<div className="button-AI-wrapper-2">
{isAnalyzing &&  <SyncLoader color="#52FF00" />}
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


        <div className="stock-market-container">
          <SymbolInfo
            colorTheme="dark"
            symbol={symbol}
            width="100%"
            //isTransparent={true}
          />
        </div>            

        <div className="chart-container">
          <AdvancedRealTimeChart 
            theme="dark" 
            hide_top_toolbar={true}
            hide_legend={true}
            withdateranges={true}
            hide_side_toolbar={true}
            symbol={symbol}
            autosize={true}
            interval="D"
            style="1"
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
   
      {showAdditionalResults && (
        <div className="additional-results-container">
          
          <div className="text-container" ref={chartSectionRef}>
              <div className="text">
                  <div className='text-style'>
                    알려주가AI가<br /> 분석한 결과에요 😎
                  </div>
                </div>
              </div>
       
          <div className="radar-chart-container">
            <div className="radar-chart">

              <Radar data={chartData} options={chartOptions} />
        
            </div>
            </div>


            <div className="model-results-container clickable-cursor" onClick={handleClick}>
              <GaugeChart id="gauge-chart3" className='gauge-chart-text' 
                style={{ width: '390px' }}
                animate={true}
                hideText={false}
                nrOfLevels={5}
                cornerRadius={0}
                arcWidth={0.06}
                arcPadding={0.015}
                percent={parseFloat(averageScorePercent.toFixed(2))}
                textColor="#ffffff"
                needleColor="#ACC2A1"
                needleBaseColor="#71985e"
                colors={["#DF5341", "#782A2B", "#ccc", "#1F3A82","#3764F3" ]}
                formatTextValue={value => value}
              />
              
            </div>
            <div className="gauge-labels">
                <span className="gauge-label left">STRONG<br />SELL</span>
                <span className="gauge-label left2">SELL</span>
                <span className="gauge-label middle">NEUTRAL</span>
                <span className="gauge-label right2">BUY</span>
                <span className="gauge-label right">STRONG<br /> BUY</span>
              </div>

              <div className="message-container">
                <div className="text">
                    <div className='text-style'>
                      {message}
                  </div>
                </div>
              </div>

              <div className="message-container-2">
                <div className="text">
                    <div className='text-style-2'>
                      인공지능이 6개의 지표를 활용하여 분석한 결과<br />[{stockLabel}]는 종합점수 {score.toFixed(0)}점으로 {marketTrend}가 예상됩니다.
                  </div>
                </div>
              </div>

              {selectedImage && (
                <div className="image-container">
                  <img className="image" src={selectedImage} alt="Result" />
                </div>
              )}
              
              

              </div>
            )}
            </div>
        </div>
  );
};
