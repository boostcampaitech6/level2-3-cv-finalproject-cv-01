import React, { useState, useEffect } from "react";
import { ButtonAi } from "../../components/ButtonAi";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { PropertyOffWrapper } from "../../components/PropertyOffWrapper";
import axios from 'axios';
import "./style.css";
import { useParams, useLocation } from "react-router-dom";
import { AdvancedRealTimeChart} from 'react-ts-tradingview-widgets';

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
      <div className="div-11">
        {/* Header section including the title "삼성전자" */}
        <div className="head-4">
          <div className="text-wrapper-37">{stockLabel}</div>
          <Heart className="heart-2" stateProp="off" />
        </div>
        <div className="chart-container">
          <AdvancedRealTimeChart 
            theme="light" 
            symbol={symbol}
            autosize={true}
            interval="D"
          />
        </div>
        {/* Content below the header */}
        <div className="content">
          <div className="market-data">
            {/* Market data here */}
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

          <ButtonAi className="button-AI-instance" stateProp="off" />
          <Menu
            className="menu-5"
            iconVariantsIconUnion="/img/union-9.png"
            to="/home"
            to1="/favorite"
            to2="/search-1"
            to3="/profile"
          />
        </div>
      </div>
    </div>
  );
};



// import React, { useState, useEffect } from "react";
// import { ButtonAi } from "../../components/ButtonAi";
// import { Heart } from "../../components/Heart";
// import { Menu } from "../../components/Menu";
// import { PropertyOffWrapper } from "../../components/PropertyOffWrapper";
// import axios from 'axios';
// import "./style.css";

// export const Result = () => {
//   const [newsData, setNewsData] = useState([]);

//   useEffect(() => {
//     const fetchNewsData = async () => {
//       try {
//         const response = await axios.get('http://localhost:8000/news/?query=삼성전자');
//         setNewsData(response.data);
//       } catch (error) {
//         console.error("Error fetching news data:", error);
//       }
//     };

//     fetchNewsData();
//   }, []);

//   return (
//     <div className="result">
//       <div className="div-11">
//         <div className="view-20">
//           <div className="frame-2">
//             <div className="text-wrapper-34">73,300</div>
//           </div>
//           <div className="frame-3">
//             <div className="text-wrapper-34">+1,100 (1.52%)</div>
//           </div>
//           <div className="frame-4">
//             <div className="text-wrapper-35">KOSPI 005930</div>
//           </div>
//           <div className="frame-5">
//             <div className="text-wrapper-35">시가총액 489.80조</div>
//           </div>
//           <div className="frame-6">
//             <div className="text-wrapper-35">시가총액 ㅇ위</div>
//           </div>
//           <img className="image-2" alt="Image" src="/img/image-99.png" />

         




//           <div className="overlap-group-5">
//             <div className="news-container">
//               {newsData.map((item, index) => (
//                 <div key={index} className="news-item">
//                   <div className="news-content">
//                     <a href={item.link} target="_blank" rel="noopener noreferrer" className="news-link">
//                       <h2 className="news-title">{item.title.replace(/<b>|<\/b>/g, '')}</h2>
//                       <p className="news-description">{item.description.replace(/<b>|<\/b>/g, '')}</p>
//                     </a>
//                   </div>
//                 </div>
//               ))}
//             </div>

//             {/* <img className="mask-group" alt="Mask group" src="/img/mask-group.png" /> */}
//             <div className="frame-7">
//               <div className="text-wrapper-36">관련 뉴스 더보기</div>
//             </div>
//             <Menu
//               className="menu-5"
//               iconVariantsIconUnion="/img/union-9.png"
//               to="/home"
//               to1="/favorite"
//               to2="/search-1"
//               to3="/profile"
//             />
//           </div>
//         </div>
//         <ButtonAi className="button-AI-instance" stateProp="off" />
//         <div className="head-4">
//           <div className="text-wrapper-37">삼성전자</div>
//           <Heart className="heart-2" stateProp="off" />
//           <PropertyOffWrapper
//             property1="off"
//             propertyOffClassName="component-1011"
//             to="/u35u4352u4455u4527u4352u4458-u4364u4453u4364u4449u4540u4370u4449u4352u4469u401u41"
//           />
//         </div>
//       </div>


//     </div>
//   );
// };
