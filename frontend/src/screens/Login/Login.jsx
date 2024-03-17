import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Login = () => {
  return (
    <div className="login">
      <div className="frame-6">
        <div className="content-2">
          <div className="demo">
            <div className="text-2">
              <div className="text-wrapper-16">데모 영상</div>
            </div>
          </div>
          <div className="container">
            <Link to="/login-kakao">
              <button className="button-2">
                <img className="kakao-logo" alt="Kakao logo" src="/img/kakao-logo.svg" />
                <div className="label-wrapper">
                  <div className="label">카카오 로그인</div>
                </div>
              </button>
            </Link>
            <Link className="text-3" to="/home">
              <div className="text-wrapper-17">로그인 없이 체험하기</div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
