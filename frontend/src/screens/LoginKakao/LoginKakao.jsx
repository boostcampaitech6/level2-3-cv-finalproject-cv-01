import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Check } from "../../components/Check";
import { useUser } from "../../components/UserContext";
import "./style.css";
import { SyncLoader } from "react-spinners";

export const LoginKakao = () => {
  const navigate = useNavigate();
  const { setUserInfo } = useUser();

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get("code");
    if (code) {
      axios.post("http://localhost:8001/auth/kakao", { code })
        .then((response) => {
          // UserContext에 사용자 정보 저장
          console.log(response.data)
          const { kakao_id, nickname, profile_image } = response.data;
          
          const formattedUserInfo = {
            kakao_id: kakao_id,
            nickname: nickname,
            profile_image: profile_image
          };

          setUserInfo(formattedUserInfo);
          
         // 1초 동안 홀딩 후 홈페이지로 이동
         setTimeout(() => {
          navigate("/home");
        }, 5000);
        })
        .catch((error) => {
          console.error("Login error:", error);
        });
    }
  }, [navigate, setUserInfo]);

  return (
    <div className="login-kakao">
      <div className="login-kakao-wrapper">
        <div className="loading-container">
          <div className="loading-text">
            <div className="loading-text-style">
            Logging in
            </div>
            </div>
          <div className="loading-p">
          <div className="loading-GIF">
            <SyncLoader color="#52FF00" />
            </div>
          </div>
          </div>
        </div>
      </div>

  );
};
