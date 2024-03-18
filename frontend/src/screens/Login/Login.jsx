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
          {/* <img className="kakao-logo" alt="Kakao logo" src="/img/2x.png" /> */}
          <div className="container">
            <div className="label" >카카오 로그인</div>
          </div>
        </a>
        <div className="frame-demo">
          <div className="text-2">
            <div className="text-wrapper-13">데모 영상</div>
          </div>
        </div>
      </div>
    </div>
  );
};

