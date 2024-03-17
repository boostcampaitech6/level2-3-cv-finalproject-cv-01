/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Component1174 = ({
  state,
  divClassName,
  divClassNameOverride,
  spanClassName,
  divClassName1,
  divClassName2,
  text = "네이버",
  logoClassName,
  to,
}) => {
  return (
    <Link className={`component-1174 state-0-${state}`} to={to}>
      <div className="div-wrapper-2">
        <div className="text-wrapper-3">-0.53%</div>
      </div>
      <div className={`div-wrapper-3 ${divClassName}`}>
        <p className={`p ${divClassNameOverride}`}>
          <span className={`span ${spanClassName}`}>188,000</span>
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
  state: PropTypes.oneOf(["off", "on"]),
  text: PropTypes.string,
  to: PropTypes.string,
};
