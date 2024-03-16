import React from "react";
import { Check } from "../../components/Check";
import "./style.css";

export const LoginKakao = () => {
  return (
    <div className="login-kakao">
      <div className="login-kakao-wrapper">
        <div className="overlap-group-wrapper">
          <div className="check-wrapper">
            <Check className="check-instance" divClassName="design-component-instance-node" />
          </div>
        </div>
      </div>
    </div>
  );
};
