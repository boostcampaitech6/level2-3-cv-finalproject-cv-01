/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Heart } from "../Heart";
import "./style.css";

export const StateOffWrapper = ({ state, className, text = "NAVER", text1 = "035420", logoClassName, to }) => {
  return (
    <Link className={`state-off-wrapper state-${state} ${className}`} to={to}>
      <div className="overlap-group">
        <div className="info">
          <div className="NAVER">{text}</div>
          <div className="text-wrapper">{text1}</div>
        </div>
        <div className={`logo ${logoClassName}`} />
        <Heart className="heart-instance" stateProp="off" />
      </div>
    </Link>
  );
};

StateOffWrapper.propTypes = {
  state: PropTypes.oneOf(["off", "on"]),
  text: PropTypes.string,
  text1: PropTypes.string,
  to: PropTypes.string,
};
