import React from "react";
import { Menu } from "../../components/Menu";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import "./style.css";

export const Favorite = () => {
  return (
    <div className="favorite">
      <div className="div-12">
        <div className="head-5">
          <div className="text-wrapper-38">FAVORITE</div>
        </div>
        <div className="div-13">
          <StateOffWrapper className="view-21" state="off" text="네이버" text1="035420" />
          <StateOffWrapper
            className="view-22"
            logoClassName="view-23"
            state="off"
            text="삼성전자"
            text1="005930"
            to="/result-1"
          />
          <StateOffWrapper className="view-22" logoClassName="view-24" state="off" text="카카오" text1="035720" />
          <StateOffWrapper className="view-25" logoClassName="view-26" state="off" text="셀트리온" text1="068270" />
        </div>
        <Menu
          className="menu-6"
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
