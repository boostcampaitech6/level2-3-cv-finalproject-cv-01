/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Component1009 = ({ state, className, divClassName, text = "네이버", logoClassName, to }) => {
  return (
    <Link className={`component-1009 state-2-${state} ${className}`} to={to}>
      <div className="div-wrapper-2">
        <div className="text-wrapper-4">-0.53%</div>
      </div>
      <div className="div-wrapper-3">
        <p className="p">
          <span className="span">188,000</span>
          <span className="text-wrapper-5">원</span>
        </p>
      </div>
      <div className={`div-wrapper-4 ${divClassName}`}>
        <div className="text-wrapper-6">{text}</div>
      </div>
      <div className={`logo-2 ${logoClassName}`} />
    </Link>
  );
};

Component1009.propTypes = {
  state: PropTypes.oneOf(["off", "on"]),
  text: PropTypes.string,
  to: PropTypes.string,
};
