import React, { useState, useEffect} from "react";
import { Link, useNavigate } from "react-router-dom";
import { Component1174 } from "../../components/Component1174";
import { Menu } from "../../components/Menu";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import { Search } from "../../components/Search";
import "./style.css";
import AsyncSelect from 'react-select/async';
import Papa from 'papaparse';

export const Home = () => {
  const navigate = useNavigate();  

  const [stocksData, setStocksData] = useState([]);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    Papa.parse("/symbol_data/korea_stock_symbols.csv", {
      download: true,
      header: true,
      delimiter: ",",
      skipEmptyLines: true,
      complete: function(results) {
        if (results.errors.length > 0) {
          // console.error("CSV 파일 로드 에러:", results.errors);
          return;
        }
        
        // console.log("CSV 파일 로딩 완료:", results.data); // 로드된 데이터 확인
        const validData = results.data.filter((row) => row.label && row.value);
        // console.log("필터링된 데이터:", validData); // 필터링된 데이터 확인
        const formattedData = validData.map((row) => ({
          label: row.label,
          value: row.value,
        }));
        setStocksData(formattedData);
      },
    });
  }, []);

  const filterOptions = (inputValue) => {
    return stocksData.filter(
      (i) => i.label && i.label.toLowerCase().includes(inputValue.toLowerCase())
    );
  };

  const handleChange = (selectedOption) => {
    if (selectedOption) {
      navigate(`/result-1/${selectedOption.value}`, {
        state: { stockLabel: selectedOption.label },
      });
    }
  };

  const loadOptions = (inputValue, callback) => {
    setTimeout(() => {
      callback(filterOptions(inputValue));
    }, 500);
  };

  const formatOptionLabel = ({ label }, { inputValue }) => {
    const parts = label.split(new RegExp(`(${inputValue})`, 'i'));
    return (
      <div>
        {parts.map((part, index) =>
          part.toLowerCase() === inputValue.toLowerCase() ? (
            <span key={index} style={{ color: '#7d49f5' }}>{part}</span>
          ) : (
            part
          )
        )}
      </div>
    );
  };

  const customStyles = {
    placeholder: (provided) => ({
      ...provided,
      fontFamily: "Noto Sans KR, Helvetica",
      paddingLeft: '10px', // 원하는 들여쓰기 값으로 조정하세요
    }),
    input: (provided) => ({
      ...provided,
      fontFamily: "Noto Sans KR, Helvetica",
      paddingLeft: '10px', // 입력 텍스트에 대한 들여쓰기
    }),
    control: (provided, { isFocused }) => ({
      ...provided,
      fontFamily: "Noto Sans KR, Helvetica",
      minHeight: '45px', // 최소 높이 설정
      borderColor: isFocused ? '#7d49f5' : provided.borderColor, // 포커스 되었을 때 보라색으로 변경
      boxShadow: isFocused ? '0 0 0 1px #7d49f5' : 'none',
    // 포커스 되었을 때 보라색 그림자 효과를 줌
      '&:hover': {
        borderColor: '#7d49f5', // 마우스 호버 시 보라색으로 변경
      },
     
    }),
    dropdownIndicator: (provided, { isFocused }) => ({
      ...provided,
      color: isFocused ? '#7d49f5':provided.color,  // 화살표 색상을 보라색으로 설정
    }),

    noOptionsMessage: (provided) => ({
      ...provided,
      fontFamily: "Noto Sans KR, Helvetica"
    }),

    loadingMessage: (provided) => ({
      ...provided,
      fontFamily: "Noto Sans KR, Helvetica"
    }),

    option: (provided, { isFocused, isSelected }) => {
      return {
        ...provided,
        backgroundColor: isSelected ? '#F2ECFF' : isFocused ? '#F2ECFF' : undefined,
        // 선택된 옵션의 배경색과 포커스 시 배경색
        fontFamily: "Noto Sans KR, Helvetica",
        paddingLeft: '20px',
      };
    },
  };

  const handleStockClick = (symbol, label) => {
    navigate(`/result/${symbol}`, { state: { stockLabel: label } });
  };

  const handleSearchClick = ( ) => {
    navigate(`/search`);
  };


  return (
    <div className="home">
      <div className="frame-8">
        <div className="content-4">
          <div className="stock-frame">
            <div className="stocks">
            <div onClick={() => handleStockClick('KRX:035420', '네이버')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-7"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                spanClassName="stock-6"
                state="off"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:068270', '셀트리온')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-10"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-9"
                spanClassName="stock-6"
                state="off"
                text="셀트리온"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:005930', '삼성전자')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-10"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-11"
                spanClassName="stock-6"
                state="off"
                text="삼성전자"
                to="/result"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:035720', '카카오')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-7"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-12"
                spanClassName="stock-6"
                state="off"
                text="카카오"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:086520', '에코프로')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-10"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-13"
                spanClassName="stock-6"
                state="off"
                text="에코프로"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:005380', '현대차')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-7"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-14"
                spanClassName="stock-6"
                state="off"
                text="현대차"
              />
            </div>
            
            <div onClick={() => handleStockClick('KRX:373220', 'LG에너지솔루션')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-30"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-15"
                spanClassName="stock-6"
                state="off"
                text="LG에너지솔루션"
              />
            </div>

            <div onClick={() => handleStockClick('KRX:000660', 'SK하이닉스')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-16"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-17"
                spanClassName="stock-6"
                state="off"
                text="SK하이닉스"
              />
            </div>
            <div onClick={() => handleStockClick('KRX:024110', '기업은행')}>
              <Component1174
                divClassName="component-1174-instance"
                divClassName1="stock-10"
                divClassName2="stock-8"
                divClassNameOverride="stock-5"
                logoClassName="stock-18"
                spanClassName="stock-6"
                state="off"
                text="기업은행"
              />
            </div>
            </div>
          </div>
          <div className="text-container">
            <div className="text-6">
              <div className="text-wrapper-26">이런 종목은 어때요?</div>
            </div>
            <div className="text-7">
              <p className="text-wrapper-27">관심 있는 주식을 클릭해 보세요.</p>
            </div>
          </div>
          <div className="container-wrapper" onClick={() => handleSearchClick()} onTouchStart={() => handleSearchClick()}>
            <div className="container-3">
            <AsyncSelect
                styles={customStyles}
                cacheOptions
                loadOptions={loadOptions}
                onInputChange={(value) => {
                  setInputValue(value);
                  return value;
                }}
                onChange={handleChange}
                placeholder="주식 종목을 입력하세요"
                formatOptionLabel={formatOptionLabel}
            />
            </div>
          </div>
          <div className="menu-wrapper">
            <Menu
              className="menu-2"
              iconVariantsIconHome="/img/home-5.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsState="off"
              iconVariantsState1="on"
              to1="/favorite"
              to2="/profile"
              to3="/search"
            />
          </div>
          <div className="head-2">
            <div className="text-wrapper-29">Home</div>
          </div>
        </div>
      </div>
    </div>
  );
};
