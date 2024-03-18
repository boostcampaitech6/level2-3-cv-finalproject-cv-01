import React, { useEffect } from 'react';
import axios from 'axios';
import { useUser } from '../../components/UserContext'; // UserContext 파일의 경로에 맞게 조정
import { Menu } from "../../components/Menu";

export const Profile = () => {
  const { userInfo, setUserInfo } = useUser(); // UserContext에서 사용자 정보 사용

  useEffect(() => {
    const fetchDetailedUserInfo = async () => {
      // UserContext에 저장된 userInfo에서 사용자 id를 사용
      if (userInfo && userInfo.id) {
        try {
          // 백엔드 API 엔드포인트에서 사용자 ID를 사용하여 요청
          const response = await axios.get(`http://localhost:8000/user/info/${userInfo.id}`);
          // 백엔드로부터 받은 상세 정보로 userInfo 상태 업데이트
          setUserInfo({ ...userInfo, ...response.data, detailedFetched: true });
        } catch (error) {
          console.error('Error fetching detailed user info:', error);
        }
      }
    };

    // detailedFetched 플래그를 사용하여 상세 정보가 이미 있는지 확인
    if (userInfo && !userInfo.detailedFetched) {
      fetchDetailedUserInfo();
    }
  }, [userInfo, setUserInfo]);

  return (
    <div className="profile">
      <div className="div-10">
        {/* 프로필 정보 표시 로직 */}
        <div className="text-wrapper-29">{userInfo ? userInfo.nickname : '게스트 사용자'}</div>
        {userInfo && (
          <>
            <div className="text-wrapper-30">사용자 닉네임: {userInfo.nickname}</div>
            <div className="text-wrapper-31">프로필 편집</div>
            <div className="overlap-group-4">
              <div className="ellipse-2" />
              {/* 이미지 주소는 예시로 사용된 것이므로 실제로 존재하는 URL을 사용하세요 */}
              <img className="image" alt="Profile" src="/img/image-120.png" />
            </div>
          </>
        )}
        <Menu
            className="menu-instance"
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
