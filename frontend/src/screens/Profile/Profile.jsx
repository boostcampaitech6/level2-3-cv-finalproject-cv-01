import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Menu } from "../../components/Menu";

export const Profile = () => {
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    // 백엔드로부터 사용자 정보를 가져오는 함수
    const fetchUserInfo = async () => {
      try {
        const response = await axios.get('http://localhost:8000/user/info'); // 백엔드 API 엔드포인트
        setUserInfo(response.data); // 상태 업데이트
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    };

    fetchUserInfo();
  }, []);

  return (
    <div className="profile">
      <div className="div-10">
        <div className="text-wrapper-29">{userInfo ? userInfo.name : '게스트 사용자'}</div>
        {userInfo && (
          <>
            <div className="text-wrapper-30">사용자 정보: {userInfo.email}</div>
            <div className="text-wrapper-31">프로필 편집</div>
            <div className="text-wrapper-32">{userInfo.username}</div>
            <div className="overlap-group-4">
              <div className="head-3">
                <div className="text-wrapper-33">Profile</div>
              </div>
              <div className="ellipse-2" />
              <img className="image" alt="Profile" src={userInfo.profileImage || "/img/image-120.png"} />
            </div>
          </>
        )}
        <img className="line" alt="Line" src="/img/line-2.png" />
        <Menu
            className="menu-instance"
            iconVariantsIconUnion="https://cdn.animaapp.com/projects/65f06d8881d354160ac5ff06/releases/65f06d961e0f8111128711d2/img/union-9@2x.png"
            to="/home"
            to1="/favorite"
            to2="/search-1"
            to3="/saved"
            to4="/profile"
          />
      </div>
    </div>
  );
};
