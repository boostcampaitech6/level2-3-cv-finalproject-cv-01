import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Login = () => {
  return (
    <div className="login">
      <div className="div-3">
        <Link className="text" to="/home">
          <div className="text-wrapper-12">로그인 없이 체험하기</div>
        </Link>
        <Link className="button-kakao-login" to="/login-kakao">
          <img className="kakao-logo" alt="Kakao logo" src="/img/2x.png" />
          <div className="container">
            <div className="label">카카오 로그인</div>
          </div>
        </Link>
        <div className="frame-demo">
          <div className="text-2">
            <div className="text-wrapper-13">데모 영상</div>
          </div>
        </div>
      </div>
    </div>
  );
};
