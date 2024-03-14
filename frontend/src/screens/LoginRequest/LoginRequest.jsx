import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const LoginRequest = () => {
  return (
    <div className="login-request">
      <div className="div-14">
        <Link className="view-27" to="/login-kakao">
          <img className="image-4" alt="Image" src="/img/2x.png" />
          <div className="label-wrapper">
            <div className="label-2">카카오 로그인</div>
          </div>
        </Link>
        <p className="text-wrapper-40">
          로그인 시 사용할 수 있는 기능,
          <br />
          혜택 정보
        </p>
      </div>
    </div>
  );
};
