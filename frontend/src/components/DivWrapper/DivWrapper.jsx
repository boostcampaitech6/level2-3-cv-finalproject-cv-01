/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const DivWrapper = ({ className, companyName, graph, symbol, price, change, percentChange, logo }) => {
  return (
    <div className={`div-wrapper ${className}`}>
      <div className="overlap-group-2">
        <div className="background">
          <img className="frame-2" alt="Frame" src={graph} />
          <div className="frame-3">
            <div className="text-wrapper-5">{price}</div>
            <div className="text-wrapper-6">{change}</div>
            <div className="text-wrapper-7">{percentChange}</div>
          </div>
        </div>
        <div className="info-2">
          <div className="text-wrapper-8">{companyName}</div>
          <div className="text-wrapper-9">{symbol}</div>
        </div>
        <img className="logo-3" alt={`${companyName} logo`} src={logo} />
      </div>
    </div>
  );
};