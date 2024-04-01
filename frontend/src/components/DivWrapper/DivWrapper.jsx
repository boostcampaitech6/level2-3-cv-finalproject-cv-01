/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const DivWrapper = ({ className, companyName, graph, symbol, price, change, volume, logo, onClick }) => {
  return (
    <div className={`div-wrapper ${className}`} onClick={onClick}>
      <div className="overlap-group-2">
        <div className="background">
          <div className="frame-2">
            <div className="text-wrapper-5">{price}</div>
          </div>
          <div className="frame-3">
            <div className="text-wrapper-6">{change}</div>
            <div className="text-wrapper-7">{volume}</div>
          </div>
        </div>
        <div className="info-2">
          <div className="text-wrapper-8">{companyName}</div>
          <div className="text-wrapper-9">{symbol}</div>
        </div>
      </div>
    </div>
  );
};