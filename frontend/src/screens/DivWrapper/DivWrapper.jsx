import React, { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Menu } from "../../components/Menu";
import { Search } from "../../components/Search";
import { StateOffWrapper } from "../../components/StateOffWrapper";
import "./style.css";
import AsyncSelect from 'react-select/async';
import Papa from 'papaparse';

export const DivWrapper = () => {
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
            <span key={index} style={{ color: 'blue' }}>{part}</span>
          ) : (
            part
          )
        )}
      </div>
    );
  };
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
          <AsyncSelect
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
    </div>
  );
};
