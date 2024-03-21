import PropTypes from "prop-types";
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { Heart } from "../Heart";
import "./style.css";

export const StateOffWrapper = ({ state, className, text, text1, logoClassName, to, onHeartClick }) => {
  const navigate = useNavigate();

  const handleHeartClick = (event) => {
    event.stopPropagation(); // 이벤트 전파를 중단합니다.
    onHeartClick(event); // onHeartClick 핸들러에 이벤트 객체를 전달합니다.
  };

  return (
    <div className={`state-off-wrapper ${className}`} onClick={() => navigate(to)}>
      <div className={`overlap-group state-${state}`}>
        <div className="info">
          <div className="NAVER">{text}</div>
          <div className="element">{text1}</div>
        </div>
        <div className={`logo ${logoClassName}`} />
        <Heart 
        className="heart-instance" 
        stateProp={state} 
        onClick={handleHeartClick} // 여기서 handleHeartClick을 연결합니다.
      />
      </div>
    </div>
  );
};

// PropTypes 추가 및 업데이트
StateOffWrapper.propTypes = {
  state: PropTypes.oneOf(["off", "on"]),
  text: PropTypes.string,
  text1: PropTypes.string,
  to: PropTypes.string,
  onHeartClick: PropTypes.func.isRequired,
};
