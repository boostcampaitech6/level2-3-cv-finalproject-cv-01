import React from "react";
import { Component1180 } from "../../components/Component1180";
import { Component1181 } from "../../components/Component1181";
import { Menu } from "../../components/Menu";
import "./style.css";

export const FavoriteWrapper = () => {
  return (
    <div className="favorite-wrapper">
      <div className="frame-29">
        <div className="content-10">
          <div className="favorite-list-2">
            <Component1180
              className="component-1180-instance"
              propertyWrapperBasesIconWrapperColorClassName="container-4"
            />
            <Component1180 className="container-5" propertyWrapperBasesIconWrapperColorClassName="container-6" />
            <Component1180 className="container-5" propertyWrapperBasesIconWrapperColorClassName="container-7" />
            <Component1180 className="container-8" propertyWrapperBasesIconWrapperColorClassName="container-9" />
          </div>
          <div className="check-box">
            <Component1181 basesIconWrapperColorClassName="component-1181-instance" property1="two" />
          </div>
          <button className="thumb-wrapper">
            <div className="thumb-2">
              <div className="label-6">
                <div className="text-wrapper-43">삭제하기</div>
              </div>
            </div>
          </button>
          <div className="menu-bar-6">
            <Menu
              className="menu-8"
              iconVariantsIconHome="/img/home-3.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsIconUser="/img/user.svg"
              iconVariantsState="off"
              iconVariantsState1="off"
              iconVariantsState2="off"
              iconVariantsState3="on"
              to="/home"
              to2="/profile"
              to3="/search"
            />
          </div>
          <div className="head-8">
            <div className="text-wrapper-44">Favorite</div>
          </div>
        </div>
      </div>
    </div>
  );
};
