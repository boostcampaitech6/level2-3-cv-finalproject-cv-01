import React from "react";
import { Link } from "react-router-dom";
import { Menu } from "../../components/Menu";
import { Search } from "../../components/Search";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import "./style.css";

export const DivWrapper = () => {
  return (
    <div className="div-wrapper">
      <div className="search-3">
        <div className="view-15">
          <div className="text-8">
            <div className="text-wrapper-27">인기 검색어</div>
          </div>
          <div className="div-9">
            <StateOffWrapper className="component-1003" state="off" text="네이버" />
            <StateOffWrapper
              className="view-16"
              logoClassName="component-1003-instance"
              state="off"
              text="삼성전자"
              text1="005930"
              to="/result-1"
            />
            <StateOffWrapper className="view-16" logoClassName="view-17" state="off" text="카카오" text1="035720" />
            <StateOffWrapper className="view-18" logoClassName="view-19" state="off" text="셀트리온" text1="068270" />
          </div>
          <Menu
            className="menu-3"
            iconVariantsIconUnion="/img/union-9.png"
            to="/home"
            to1="/favorite"
            to2="/search-1"
            to3="/profile"
          />
        </div>
        <div className="serch-wrapper">
          <Link className="serch-3" to="/search-2">
            <div className="text-9">
              <div className="text-wrapper-28">주식 종목을 입력하세요</div>
            </div>
            <Search className="icon-search-2" />
          </Link>
        </div>
      </div>
    </div>
  );
};
