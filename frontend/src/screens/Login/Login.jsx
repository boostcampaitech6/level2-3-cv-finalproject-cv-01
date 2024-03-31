import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Login = () => {
  const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.REACT_APP_KAKAO_CLIENT_ID}&redirect_uri=${encodeURIComponent(process.env.REACT_APP_KAKAO_REDIRECT_URI)}&response_type=code`;
  
  return (
    <div className="login">
      <div className="frame-6">
        <div className="demo-container">
           <div className="demo">
          {/* 데모 영상이 표시됩니다 */}
         </div>
         </div>
        <div className="demo-txt-container">
          <div className="text-2">
          <div className="text-wrapper-16">demo</div>
        </div>
        </div>

      <div className="login-button-container">
        <a href={KAKAO_AUTH_URL} className="button-kakao-login">
          <button className="button-2">
            <img className="kakao-logo" alt="Kakao logo" src="/img/kakao-logo.svg" />
            <div className="label-wrapper">
              <div className="label">카카오 로그인</div>
            </div>
          </button>
        </a>
        <Link className="text-3" to="/home">
          <div className="text-wrapper-17">로그인 없이 체험하기</div>
        </Link>
      </div>
    </div>
    </div>
);
};
