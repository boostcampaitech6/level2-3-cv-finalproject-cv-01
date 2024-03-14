import React from "react";
import { Check } from "../../components/Check";
import "./style.css";

export const LoginKakao = () => {
  return (
    <div className="login-kakao">
      <div className="login-kakao-wrapper">
        <div className="overlap-group-wrapper-2">
          <div className="check-wrapper">
            <Check className="check-instance" divClassName="check-2" />
          </div>
        </div>
      </div>
    </div>
  );
};
