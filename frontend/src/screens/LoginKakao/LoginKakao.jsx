import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./style.css";

export const LoginKakao = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // URL에서 인증 코드(code) 추출
    const code = new URLSearchParams(window.location.search).get("code");

    if (code) {
      // 인증 코드를 서버로 전송하고 로그인 처리
      axios.post("http://localhost:8002/auth/kakao", { code })
        .then((response) => {
          // 서버로부터 로그인 처리 응답 받음
          console.log("Login response:", response.data);
          // 홈 화면으로 리디렉션
          navigate("/home");
        })
        .catch((error) => {
          console.error("Login error:", error);
          // 에러 처리, 필요에 따라 에러 페이지로 리디렉션할 수 있음
        });
    }
  }, [navigate]);

  return (
    <div className="login-kakao">
      <div className="loading-text">로그인 중...</div>
    </div>
  );
};
