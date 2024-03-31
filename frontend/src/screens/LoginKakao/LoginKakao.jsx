import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Check } from "../../components/Check";
import { useUser } from "../../components/UserContext";
import "./style.css";

export const LoginKakao = () => {
  const navigate = useNavigate();
  const { setUserInfo } = useUser();

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get("code");
    if (code) {
      axios.post("http://localhost:8000/auth/kakao", { code })
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
          navigate("/home");
        })
        .catch((error) => {
          console.error("Login error:", error);
        });
    }
  }, [navigate, setUserInfo]);

  return (
    <div className="login-kakao">
      <div className="loading-text">로그인 중...</div>
      <div className="login-kakao-wrapper">
        <div className="overlap-group-wrapper">
          <div className="check-wrapper">
            <Check className="check-instance" divClassName="design-component-instance-node" />
          </div>
        </div>
      </div>
    </div>
  );
};
