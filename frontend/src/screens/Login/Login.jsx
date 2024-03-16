import React from "react";
import "./style.css";

export const Login = () => {
  const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.REACT_APP_KAKAO_CLIENT_ID}&redirect_uri=${encodeURIComponent(process.env.REACT_APP_KAKAO_REDIRECT_URI)}&response_type=code`;

  return (
    <div className="login">
      <div className="div-3">
        <a href="/home" className="text">
          <div className="text-wrapper-12">로그인 없이 체험하기</div>
        </a>
        <a href={KAKAO_AUTH_URL} className="button-kakao-login">
          <img className="kakao-logo" alt="Kakao logo" src="/img/2x.png" />
          <div className="container">
            <div className="label">카카오 로그인</div>
          </div>
        </a>
        <div className="frame-demo">
          <div className="text-2">
            <div className="text-wrapper-13">데모 영상</div>
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
