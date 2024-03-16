/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const DivWrapper = ({ className }) => {
  return (
    <div className={`div-wrapper ${className}`}>
      <div className="overlap-group-2">
        <div className="background">
          <img className="frame-2" alt="Frame" src="/img/frame-40.svg" />
          <div className="frame-3">
            <div className="text-wrapper-5">188,000 원</div>
            <div className="text-wrapper-6">- 1,000</div>
            <div className="text-wrapper-7">- 0.53%</div>
          </div>
        </div>
        <div className="info-2">
          <div className="text-wrapper-8">NAVER</div>
          <div className="text-wrapper-9">035420</div>
        </div>
        <div className="logo-3" />
      </div>
    </div>
  );
};
