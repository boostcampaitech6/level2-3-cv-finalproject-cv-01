import React from "react";
import { Menu } from "../../components/Menu";
import "./style.css";

export const Profile = () => {
  return (
    <div className="profile">
      <div className="div-10">
        <div className="text-wrapper-29">게스트 사용자</div>
        <div className="text-wrapper-30">사용자 정보</div>
        <div className="text-wrapper-31">프로필 편집</div>
        <div className="text-wrapper-32">주린이1230124</div>
        <div className="overlap-group-4">
          <div className="head-3">
            <div className="text-wrapper-33">Profile</div>
          </div>
          <div className="ellipse-2" />
          <img className="image" alt="Image" src="/img/image-120.png" />
        </div>
        <img className="line" alt="Line" src="/img/line-2.png" />
        <Menu
          className="menu-4"
          iconVariantsIconUnion="/img/union-9.png"
          to="/home"
          to1="/favorite"
          to2="/search-1"
          to3="/profile"
        />
      </div>
    </div>
  );
};
