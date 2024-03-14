import React from "react";
import { Heart } from "../../components/Heart";
import { Menu } from "../../components/Menu";
import { PropertyOffWrapper } from "../../components/PropertyOffWrapper";
import "./style.css";

export const Screen14 = () => {
  return (
    <div className="screen-14">
      <div className="result-3">
        <div className="overlap-group-7">
          <div className="view-29">
            <div className="frame-14">
              <div className="text-wrapper-45">73,300</div>
            </div>
            <div className="frame-15">
              <div className="text-wrapper-45">+1,100 (1.52%)</div>
            </div>
            <div className="frame-16">
              <div className="text-wrapper-46">KOSPI 005930</div>
            </div>
            <div className="frame-17">
              <div className="text-wrapper-46">시가총액 489.80조</div>
            </div>
            <div className="frame-18">
              <div className="text-wrapper-46">시가총액 ㅇ위</div>
            </div>
            <img className="image-6" alt="Image" src="/img/image-99.png" />
            <img className="mask-group-3" alt="Mask group" src="/img/mask-group.png" />
            <div className="frame-19">
              <div className="text-wrapper-47">관련 뉴스 더보기</div>
            </div>
            <Menu
              className="menu-8"
              iconVariantsIconUnion="/img/union-9.png"
              to="/home"
              to1="/favorite"
              to2="/search-1"
              to3="/profile"
            />
            <button className="button">
              <div className="text-wrapper-48">분석 결과 저장하기</div>
            </button>
          </div>
          <div className="view-30">
            <div className="AI-wrapper">
              <div className="AI-3">AI가&nbsp;&nbsp;분석한 결과에요</div>
            </div>
            <img className="image-7" alt="Image" src="/img/image-106.png" />
            <img className="image-8" alt="Image" src="/img/image-18.png" />
            <div className="frame-20">
              <div className="text-wrapper-49">삼성전자 분석 총평</div>
            </div>
            <div className="element-THIS-IS-wrapper">
              <p className="element-THIS-IS">
                2024년 3월 10일 .....
                <br />
                내용내용 THIS IS 내용
                <br />
                내용내용 THIS IS 내용
                <br />
                내용내용 THIS IS 내용
                <br />
                내용내용 THIS IS 내용
                <br />
                내용내용 THIS IS 내용
              </p>
            </div>
          </div>
        </div>
        <div className="head-7">
          <div className="text-wrapper-50">삼성전자</div>
          <Heart className="heart-4" stateProp="off" />
          <PropertyOffWrapper property1="on" propertyOffClassName="image-9" to="/share" />
        </div>
      </div>
    </div>
  );
};
