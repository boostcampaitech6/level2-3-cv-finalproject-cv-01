/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const PropertyOffWrapper = ({ property1, propertyOffClassName, to }) => {
  return (
    <Link to={to}>
      <img
        className={`property-off-wrapper ${propertyOffClassName}`}
        alt="Property off"
        src={property1 === "on" ? "/img/property-1-on.png" : "/img/property-1-off.png"}
      />
    </Link>
  );
};

PropertyOffWrapper.propTypes = {
  property1: PropTypes.oneOf(["off", "on"]),
  to: PropTypes.string,
};
