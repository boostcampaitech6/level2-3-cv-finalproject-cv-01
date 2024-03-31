/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const HeartOn = ({ color = "#7D49F5", className }) => {
  return (
    <svg
      className={`heart-on ${className}`}
      fill="none"
      height="24"
      viewBox="0 0 24 24"
      width="24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        className="path"
        d="M3.54158 4.61204C1.48614 6.76143 1.48614 10.2463 3.54158 12.3957L11.6071 20.8298C11.8241 21.0567 12.1759 21.0567 12.3929 20.8298L20.4584 12.3957C22.5139 10.2463 22.5139 6.76143 20.4584 4.61204C18.403 2.46265 15.0705 2.46265 13.015 4.61204L12 5.67344L10.985 4.61204C8.92955 2.46265 5.59702 2.46265 3.54158 4.61204Z"
        fill={color}
      />
    </svg>
  );
};

HeartOn.propTypes = {
  color: PropTypes.string,
};
