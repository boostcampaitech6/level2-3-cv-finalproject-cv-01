import React, { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Menu } from "../../components/Menu";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import { Heart } from "../../components/Heart";
import "./style.css";
import AsyncSelect from 'react-select/async';
import Papa from 'papaparse';

export const SearchScreen = () => {
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
      paddingLeft: '10px', // 원하는 들여쓰기 값으로 조정하세요
    }),
    input: (provided) => ({
      ...provided,
      paddingLeft: '10px', // 입력 텍스트에 대한 들여쓰기
    }),
    control: (provided, { isFocused }) => ({
      ...provided,
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

    option: (provided, { isFocused, isSelected }) => {
      return {
        ...provided,
        backgroundColor: isSelected ? '#F2ECFF' : isFocused ? '#F2ECFF' : undefined,
        // 선택된 옵션의 배경색과 포커스 시 배경색
        paddingLeft: '20px',
      };
    },
  };

  const handleStockClick = (symbol, label) => {
    navigate(`/result/${symbol}`, { state: { stockLabel: label } });
  };

  const [likes, setLikes] = useState({}); // 각 주식의 '좋아요' 상태를 관리합니다.

  const toggleLike = (symbol) => {
    setLikes((currentLikes) => ({
      ...currentLikes,
      [symbol]: !currentLikes[symbol], // 토글된 상태를 저장합니다.
    }));
  };


  return (
    <div className="search-screen">
      <div className="frame-7">
        <div className="content-3">
          <div className="stock-list">
          <div onClick={() => handleStockClick('KRX:035420', '네이버')}>
            <StateOffWrapper 
              className="component-1169-instance" 
              logoClassName="logo-img"
              state={likes['KRX:035420'] ? 'on' : 'off'} 
              text="네이버"
              text1="035420"
              onHeartClick={() => toggleLike('KRX:035420')} // onHeartClick prop 추가
            />
          </div>

          <div onClick={() => handleStockClick('KRX:005930', '삼성전자')}>
            <StateOffWrapper
                className="component-1169-instance"
                logoClassName="component-1169"
                state={likes['KRX:005930'] ? 'on' : 'off'}
                text="삼성전자"
                text1="005930"
                onHeartClick={() => toggleLike('KRX:005930')}
              />
          </div>

          <div onClick={() => handleStockClick('KRX:035720', '카카오')}>
            <StateOffWrapper
                className="component-1169-instance"
                logoClassName="stock-2"
                state={likes['KRX:035720'] ? 'on' : 'off'}
                text="카카오"
                text1="035720"
                onHeartClick={() => toggleLike('KRX:035720')}
              />
          </div>
            
          <div onClick={() => handleStockClick('KRX:068270', '셀트리온')}>
            <StateOffWrapper 
              className="component-1169-instance" 
              logoClassName="stock-4" 
              state={likes['KRX:068270'] ? 'on' : 'off'} 
              text="셀트리온" 
              text1="068270" 
              onHeartClick={() => toggleLike('KRX:068270')}
            />
          </div>

          </div>
          <div className="text-4">
            <div className="text-wrapper-18">인기 검색어</div>
          </div>
          <div className="search-bar">
            <div className="container-2">
              <AsyncSelect
              autoFocus
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
          <div className="menu-bar">
            <Menu
              className="menu-instance"
              iconVariantsIconHome="/img/home-3.svg"
              iconVariantsIconUnion="/img/union-9.svg"
              iconVariantsState="on"
              to="/home"
              to1="/favorite"
              to2="/profile"
            />
          </div>
          <div className="head">
            <div className="text-wrapper-20">Search</div>
          </div>
        </div>
      </div>
    </div>
  );
};
