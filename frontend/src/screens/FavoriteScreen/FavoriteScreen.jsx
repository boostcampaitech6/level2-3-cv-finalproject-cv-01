import React from "react";
import { Link } from "react-router-dom";
import { DivWrapper } from "../../components/DivWrapper";
import { Menu } from "../../components/Menu";
import "./style.css";

export const FavoriteScreen = () => {
  return (
    <div className="favorite-screen">
      <div className="frame-10">
        <div className="content-6">
          <div className="button-3">
            <Link to="/search">
              <img className="img-2" alt="Plus" src="/img/plus.svg" />
            </Link>
            <Link to="/favorite-2">
              <img className="img-2" alt="Minus" src="/img/minus.svg" />
            </Link>
          </div>
          <div className="favorite-list">
            <DivWrapper
              className="component-1175"
              companyName="네이버"
              symbol="035420"
              price="184,100 원"
              change="-2,000"
              percentChange="-1.07%"
              graph="/img/frame-40.svg" 
              logo="/img/ellipse-15.png"
            />
            <DivWrapper
              className="component-1175"
              companyName="삼성전자"
              symbol="005930"
              price="72,800 원"
              change="+5,00"
              percentChange="+0.69%"
              graph="/img/frame-40.svg" 
              logo="/img/ellipse-15-1.png"
            />
            <DivWrapper
              className="component-1175"
              companyName="카카오"
              symbol="035720"
              price="53,000 원"
              change="-1,100"
              percentChange="-2.03%"
              graph="/img/frame-40.svg" 
              logo="/img/ellipse-15-9.png"
            />
          </div>
          <div className="menu-bar-2">
            <Menu
              className="menu-4"
              iconVariantsIconHome="/img/home-7.svg"
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
          <div className="head-4">
            <div className="text-wrapper-33">Favorite</div>
          </div>
        </div>
      </div>
    </div>
  );
};
