import React from "react";
import { Menu } from "../../components/Menu";
import "./style.css";

export const Profile = () => {
  return (
    <div className="profile">
      <div className="frame-9">
        <div className="content-5">
          <div className="label-2">
            <div className="text-wrapper-30">주린이1230124</div>
          </div>
          <div className="label-3">
            <div className="text-wrapper-30">게스트 사용자</div>
          </div>
          <div className="overlap">
            <div className="overlap-2">
              <div className="overlap-group-4">
                <div className="label-4">
                  <div className="text-wrapper-30">사용자 정보</div>
                </div>
                <div className="line">
                  <img className="line-2" alt="Line" src="/img/line-2.svg" />
                </div>
              </div>
              <div className="img-frame">
                <div className="ellipse-2" />
                <img className="image-2" alt="Image" src="/img/image-120.png" />
              </div>
            </div>
            <div className="label-5">
              <div className="text-wrapper-31">프로필 편집</div>
            </div>
          </div>
          <div className="menu-instance-wrapper">
            <Menu
              className="menu-3"
              iconVariantsIconHome="/img/home-3.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsIconUser="/img/user-6.svg"
              iconVariantsState="off"
              iconVariantsState1="off"
              iconVariantsState2="on"
              to="/home"
              to1="/favorite"
              to3="/search"
            />
          </div>
          <div className="head-3">
            <div className="text-wrapper-32">Profile</div>
          </div>
        </div>
      </div>
    </div>
  );
};
