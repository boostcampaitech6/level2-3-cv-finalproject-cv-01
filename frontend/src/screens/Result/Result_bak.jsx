import React from "react";
import { ButtonAi } from "../../components/ButtonAi";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { PropertyOffWrapper } from "../../components/PropertyOffWrapper";
import "./style.css";


export const Result = () => {
  return (
    <div className="result">
      <div className="div-11">
        <div className="view-20">
          <div className="frame-2">
            <div className="text-wrapper-34">73,300</div>
          </div>
          <div className="frame-3">
            <div className="text-wrapper-34">+1,100 (1.52%)</div>
          </div>
          <div className="frame-4">
            <div className="text-wrapper-35">KOSPI 005930</div>
          </div>
          <div className="frame-5">
            <div className="text-wrapper-35">시가총액 489.80조</div>
          </div>
          <div className="frame-6">
            <div className="text-wrapper-35">시가총액 ㅇ위</div>
          </div>
          <img className="image-2" alt="Image" src="/img/image-99.png" />
          <div className="overlap-group-5">
            <img className="mask-group" alt="Mask group" src="/img/mask-group.png" />
            <div className="frame-7">
              <div className="text-wrapper-36">관련 뉴스 더보기</div>
            </div>
            <Menu
              className="menu-5"
              iconVariantsIconUnion="/img/union-9.png"
              to="/home"
              to1="/favorite"
              to2="/search-1"
              to3="/profile"
            />
          </div>
        </div>
        <ButtonAi className="button-AI-instance" stateProp="off" />
        <div className="head-4">
          <div className="text-wrapper-37">삼성전자</div>
          <Heart className="heart-2" stateProp="off" />
          <PropertyOffWrapper
            property1="off"
            propertyOffClassName="component-1011"
            to="/u35u4352u4455u4527u4352u4458-u4364u4453u4364u4449u4540u4370u4449u4352u4469u401u41"
          />
        </div>
      </div>
    </div>
  );
};
