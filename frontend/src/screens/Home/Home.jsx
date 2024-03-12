import React from "react";
import { Link } from "react-router-dom";
import { Component1009 } from "../../components/Component1009";
import { Menu } from "../../components/Menu";
import { Search } from "../../components/Search";
import "./style.css";

export const Home = () => {
  return (
    <div className="home">
      <div className="div-5">
        <div className="div-6">
          <div className="overlap-group-3">
            <div className="text-5">
              <p className="text-wrapper-18">관심 있는 주식을 클릭해 보세요.</p>
            </div>
            <div className="text-6">
              <div className="text-wrapper-19">이런 종목은 어때요?</div>
            </div>
          </div>
          <Link className="serch-2" to="/search-1">
            <div className="text-7">
              <div className="text-wrapper-20">주식 종목을 입력하세요</div>
            </div>
            <Search className="search-instance" />
          </Link>
          <div className="overlap">
            <div className="view-wrapper">
              <div className="view-4">
                <Component1009 className="component-1009-instance" state="off" />
                <Component1009
                  className="component-1009-instance"
                  divClassName="view-5"
                  logoClassName="view-6"
                  state="off"
                  text="셀트리온"
                />
                <Component1009
                  className="component-1009-instance"
                  divClassName="view-5"
                  logoClassName="view-7"
                  state="off"
                  text="삼성전자"
                  to="/result-1"
                />
                <Component1009 className="component-1009-instance" logoClassName="view-8" state="off" text="카카오" />
                <Component1009
                  className="component-1009-instance"
                  divClassName="view-5"
                  logoClassName="view-9"
                  state="off"
                  text="에코프로"
                />
                <Component1009 className="component-1009-instance" logoClassName="view-10" state="off" text="현대차" />
                <div className="LG">
                  <div className="view-11">
                    <div className="text-wrapper-21">-0.53%</div>
                  </div>
                  <div className="view-12">
                    <p className="div-7">
                      <span className="text-wrapper-22">188,000</span>
                      <span className="text-wrapper-23">원</span>
                    </p>
                  </div>
                  <div className="view-13">
                    <p className="div-8">
                      <span className="text-wrapper-24">LG에너</span>
                      <span className="text-wrapper-25">지</span>
                      <span className="text-wrapper-24">솔루션</span>
                    </p>
                  </div>
                  <div className="logo-5" />
                </div>
                <Component1009
                  className="component-1009-instance"
                  divClassName="SK"
                  logoClassName="SK-2"
                  state="off"
                  text="SK하이닉스"
                />
                <Component1009
                  className="component-1009-instance"
                  divClassName="view-5"
                  logoClassName="view-14"
                  state="off"
                  text="기업은행"
                />
              </div>
            </div>
            <Menu
              className="menu-2"
              iconVariantsIconUnion="/img/union-9.png"
              to="/home"
              to1="/favorite"
              to2="/search-1"
              to3="/profile"
            />
          </div>
        </div>
        <div className="head-2">
          <div className="text-wrapper-26">Home</div>
        </div>
      </div>
    </div>
  );
};
