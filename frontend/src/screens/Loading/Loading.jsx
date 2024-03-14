import React from "react";
import { Link } from "react-router-dom";
import { Loding } from "../../components/Loding";
import "./style.css";

export const Loading = () => {
  return (
    <div className="loading">
      <Link className="div-2" to="/login">
        <Loding className="loding-2" frame="one" />
        <div className="AI">
          <div className="AI-2">
            <div className="text-wrapper-9">알려주가</div>
            <div className="text-wrapper-10">AI</div>
          </div>
          <p className="text-wrapper-11">- 쉽고 간편한 AI 주가 예측 서비스</p>
        </div>
      </Link>
    </div>
  );
};
