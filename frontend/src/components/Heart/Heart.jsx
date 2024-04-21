/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/


import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const Heart = ({ stateProp, onClick }) => {
  const handleClick = (event) => {
    event.stopPropagation(); // 이벤트 전파를 중단합니다.
    onClick(); // onClick 핸들러 실행
  };

  return (
    <div
      className={`heart ${stateProp === "on" ? "heart-5" : "heart-4"}`}
      onClick={handleClick}
    />
  );
};

Heart.propTypes = {
  stateProp: PropTypes.oneOf(["off", "on"]).isRequired,
  onClick: PropTypes.func.isRequired,
};
