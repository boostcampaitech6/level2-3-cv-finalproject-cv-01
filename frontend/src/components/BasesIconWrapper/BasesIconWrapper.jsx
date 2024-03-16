/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const BasesIconWrapper = ({ className, colorClassName, color = "/img/color-2.svg" }) => {
  return (
    <div className={`bases-icon-wrapper ${className}`}>
      <img className={`color ${colorClassName}`} alt="Color" src={color} />
    </div>
  );
};

BasesIconWrapper.propTypes = {
  color: PropTypes.string,
};
