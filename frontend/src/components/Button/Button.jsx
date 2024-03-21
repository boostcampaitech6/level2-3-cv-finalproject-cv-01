/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const Button = ({ state, className }) => {
  return (
    <div className={`button state-6-${state} ${className}`}>
      <div className="div-2">
        {state === "off" && <>분석 결과 공유하기</>}

        {state === "on" && <>분석 결과 공유하기</>}
      </div>
    </div>
  );
};

Button.propTypes = {
  state: PropTypes.oneOf(["off", "on"]),
};
