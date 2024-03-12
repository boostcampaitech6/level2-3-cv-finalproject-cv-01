import React from "react";
import { Link } from "react-router-dom";
import { Heart } from "../../components/Heart";
import { Loding } from "../../components/Loding";
import { Menu } from "../../components/Menu";
import { PropertyOffWrapper } from "../../components/PropertyOffWrapper";
import "./style.css";

export const ResultScreen = () => {
  return (
    <div className="result-screen">
      <Link className="result-2" to="/result-3">
        <div className="view-28">
          <div className="frame-8">
            <div className="text-wrapper-41">73,300</div>
          </div>
          <div className="frame-9">
            <div className="text-wrapper-41">+1,100 (1.52%)</div>
          </div>
          <div className="frame-10">
            <div className="text-wrapper-42">KOSPI 005930</div>
          </div>
          <div className="frame-11">
            <div className="text-wrapper-42">시가총액 489.80조</div>
          </div>
          <div className="frame-12">
            <div className="text-wrapper-42">시가총액 ㅇ위</div>
          </div>
          <img className="image-5" alt="Image" src="/img/image-99.png" />
          <div className="overlap-group-6">
            <img className="mask-group-2" alt="Mask group" src="/img/mask-group.png" />
            <div className="frame-13">
              <div className="text-wrapper-43">관련 뉴스 더보기</div>
            </div>
            <Loding
              className="loding-2-instance"
              ellipse="/img/ellipse-2-4.png"
              ellipseClassName="loding-instance"
              frame="one"
            />
            <Menu
              className="menu-7"
              iconVariantsIconUnion="/img/union-9.png"
              to="/home"
              to1="/favorite"
              to2="/search-1"
              to3="/profile"
            />
          </div>
        </div>
        <div className="head-6">
          <div className="text-wrapper-44">삼성전자</div>
          <Heart className="heart-3" stateProp="off" />
          <PropertyOffWrapper property1="off" propertyOffClassName="component-1011-instance" />
        </div>
      </Link>
    </div>
  );
};
