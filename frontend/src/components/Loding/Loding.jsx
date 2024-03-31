/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const Loding = ({ frame, className, ellipse = "/img/ellipse-2-3.svg" }) => {
  return (
    <div className={`loding ${className}`}>
      <div className="group">
        <img
          className={`ellipse frame-${frame}`}
          alt="Ellipse"
          src={
            frame === "three"
              ? "/img/ellipse-2-1.svg"
              : frame === "two"
              ? "/img/ellipse-2-2.svg"
              : frame === "one"
              ? ellipse
              : "/img/ellipse-2.svg"
          }
        />
      </div>
    </div>
  );
};

Loding.propTypes = {
  frame: PropTypes.oneOf(["two", "one", "three", "four"]),
  ellipse: PropTypes.string,
};
