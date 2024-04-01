import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { Link } from "react-router-dom";
import "./style.css";

export const Component1174 = ({
  symbol, // 종목 코드를 받는 새로운 prop
  state,
  divClassName,
  divClassNameOverride,
  spanClassName,
  divClassName1,
  divClassName2,
  text,
  logoClassName,
  to,
}) => {
  const [stockInfo, setStockInfo] = useState(() => {
    // 로컬 캐시에서 이전 주식 정보를 가져옵니다
    const cachedInfo = sessionStorage.getItem(symbol);
    return cachedInfo ? JSON.parse(cachedInfo) : { change: "", price: "" };
  });

  useEffect(() => {
    const fetchStockData = async () => {
      // 캐시된 정보가 없으면 새로 가져옵니다
      if (!sessionStorage.getItem(symbol)) {
        try {
          const response = await axios.get(`http://${process.env.SERVER_IP}:${process.env.PORT}/api/stock/${symbol}`);
          const data = response.data;
          const changeFormatted = (data.change * 100).toFixed(2);
          const newInfo = { change: changeFormatted, price: data.close };
          setStockInfo(newInfo);
          sessionStorage.setItem(symbol, JSON.stringify(newInfo)); // 새 정보를 세션 스토리지에 저장
        } catch (error) {
          console.error("주식 정보 가져오기 실패:", error);
        }
      }
    };

    if (symbol) {
      fetchStockData();
    }
  }, [symbol]);

   // 변동률에 따른 클래스 이름 동적 결정
   const changeClassName = stockInfo.change >= 0 ? "text-wrapper-5" : "text-wrapper-3";

  return (
    <Link className={`component-1174 state-0-${state}`} to={to || "#"}>
      <div className="div-wrapper-2">
        <div className={changeClassName}>{stockInfo.change}%</div>
      </div>
      <div className={`div-wrapper-3 ${divClassName}`}>
        <p className={`p`}>
          <span className={`span`}>{stockInfo.price}</span>
          <span className="text-wrapper-45">원</span>
        </p>
      </div>
      <div className={`div-wrapper-4 ${divClassName1}`}>
        <div className={`text-wrapper-4 ${divClassName2}`}>{text}</div>
      </div>
      <div className={`logo-2 ${logoClassName}`} />
    </Link>
  );
};

Component1174.propTypes = {
  symbol: PropTypes.string.isRequired, // 종목 코드 prop 추가
  state: PropTypes.oneOf(["off", "on"]),
  text: PropTypes.string,
  to: PropTypes.string,
};