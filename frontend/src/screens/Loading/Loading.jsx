import React from "react";
import { SyncLoader } from "react-spinners";
import { Link } from "react-router-dom";
import { Loding } from "../../components/Loding";
import "./style.css";

export const Loading = () => {
  return (
    <Link className="loading" to="/login">
      <div className="content-wrapper">
        <div className="content">
          <div className="title">
            <div className="service-name">
              <div className="t">알려주가</div>
              <div className="t-2">AI</div>
            </div>
            <p className="text">- 쉽고 간편한 AI 주가 예측 서비스</p>
          </div>
          <div className="loading-GIF">
            <SyncLoader color="#7d49f5" />
            </div>
        </div>
      </div>
    </Link>
  );
};
