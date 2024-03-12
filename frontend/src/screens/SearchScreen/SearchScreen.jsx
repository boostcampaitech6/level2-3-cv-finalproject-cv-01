import React from "react";
import { Link } from "react-router-dom";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { Search } from "../../components/Search";
import "./style.css";

export const SearchScreen = () => {
  return (
    <div className="search-screen">
      <div className="search-2">
        <div className="view">
          <div className="text-3">
            <div className="text-wrapper-14">검색 결과</div>
          </div>
          <div className="div-4">
            <div className="overlap-group-wrapper">
              <div className="overlap-group-2">
                <div className="info-2">
                  <p className="NAVER-2">
                    <span className="text-wrapper-15">삼성</span>
                    <span className="text-wrapper-16">제약</span>
                  </p>
                  <div className="element-2">001360</div>
                </div>
                <div className="logo-3" />
                <Heart className="design-component-instance-node" stateProp="off" />
              </div>
            </div>
            <Link className="overlap-wrapper" to="/result-1">
              <div className="overlap-group-2">
                <div className="info-2">
                  <p className="NAVER-2">
                    <span className="text-wrapper-15">삼성</span>
                    <span className="text-wrapper-16">전자</span>
                  </p>
                  <div className="element-2">005930</div>
                </div>
                <div className="logo-4" />
                <Heart className="design-component-instance-node" stateProp="off" />
              </div>
            </Link>
            <div className="view-2">
              <div className="overlap-group-2">
                <div className="info-2">
                  <p className="NAVER-2">
                    <span className="text-wrapper-15">삼성</span>
                    <span className="text-wrapper-16">전기</span>
                  </p>
                  <div className="element-2">009105</div>
                </div>
                <div className="logo-4" />
                <Heart className="design-component-instance-node" stateProp="off" />
              </div>
            </div>
            <div className="view-3">
              <div className="overlap-group-2">
                <div className="info-2">
                  <p className="NAVER-2">
                    <span className="text-wrapper-15">삼성</span>
                    <span className="text-wrapper-16">증권</span>
                  </p>
                  <div className="element-2">016360</div>
                </div>
                <div className="logo-4" />
                <Heart className="design-component-instance-node" stateProp="off" />
              </div>
            </div>
          </div>
          <Menu
            className="menu-instance"
            iconVariantsIconUnion="/img/union-9.png"
            to="/home"
            to1="/favorite"
            to2="/search-1"
            to3="/profile"
          />
        </div>
        <div className="head">
          <div className="serch">
            <div className="text-4">
              <div className="text-wrapper-17">삼성</div>
            </div>
            <Search className="icon-search" />
          </div>
        </div>
      </div>
    </div>
  );
};
