import React from "react";
import { Link } from "react-router-dom";
import { Menu } from "../../components/Menu";
import { Search } from "../../components/Search";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import "./style.css";

export const Home = () => {
  return (
    <div className="home">
      <div className="div-2">
        <div className="div-3">
          <div className="overlap-group-2">
            <div className="text">
              <p className="text-wrapper-6">관심 있는 주식을 클릭해 보세요.</p>
            </div>
            <div className="text-2">
              <div className="text-wrapper-7">이런 종목은 어때요?</div>
            </div>
          </div>
          <Link className="serch" to="/search-1">
            <div className="text-3">
              <div className="text-wrapper-8">주식 종목을 입력하세요</div>
            </div>
            <Search className="icon-search" />
          </Link>
          <div className="overlap">
            <div className="view">
              <StateOffWrapper className="component-993" state="off" />
              <StateOffWrapper
                className="component-993"
                divClassName="component-993-instance"
                logoClassName="design-component-instance-node"
                state="off"
                text="셀트리온"
              />
              <StateOffWrapper
                className="component-993"
                divClassName="component-993-instance"
                logoClassName="view-2"
                state="off"
                text="삼성전자"
              />
              <StateOffWrapper className="component-993" logoClassName="view-3" state="off" text="카카오" />
              <StateOffWrapper
                className="component-993"
                divClassName="component-993-instance"
                logoClassName="view-4"
                state="off"
                text="에코프로"
              />
              <StateOffWrapper className="component-993" logoClassName="view-5" state="off" text="현대차" />
              <div className="LG">
                <div className="view-6">
                  <div className="text-wrapper-9">-0.53%</div>
                </div>
                <div className="view-7">
                  <p className="div-4">
                    <span className="text-wrapper-10">188,000</span>
                    <span className="text-wrapper-11">원</span>
                  </p>
                </div>
                <div className="view-8">
                  <p className="div-5">
                    <span className="text-wrapper-12">LG에너</span>
                    <span className="text-wrapper-13">지</span>
                    <span className="text-wrapper-12">솔루션</span>
                  </p>
                </div>
                <div className="logo-3" />
              </div>
              <StateOffWrapper
                className="component-993"
                divClassName="SK"
                logoClassName="SK-2"
                state="off"
                text="SK하이닉스"
              />
              <StateOffWrapper
                className="component-993"
                divClassName="component-993-instance"
                logoClassName="view-9"
                state="off"
                text="기업은행"
              />
            </div>
          </div>
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
        <div className="head">
          <div className="text-wrapper-14">Home</div>
        </div>
      </div>
    </div>
  );
};
