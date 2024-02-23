import { FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Prediction.module.css";
// import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets"; 
import Select from 'react-select';
import React, { useState } from 'react';
import { companyOptions, periodOptions, intervalOptions } from '../docs/prediction_data';

const Prediction: FunctionComponent = () => {
  const navigate = useNavigate();

  const onHomeContainerClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onAboutUsContainerClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);

  const handlePredictClick = () => {
    console.log("Predict button clicked");
    // 여기에 예측 로직 또는 다른 동작을 추가할 수 있습니다.
  };

  const [isClearable, setIsClearable] = useState(true);
  const [isSearchable, setIsSearchable] = useState(true);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRtl, setIsRtl] = useState(false);

  return (
    <div className={styles.prediction}>
      <div className={styles.menuBar}> {/* menuBar div 추가 */}
        <div className={styles.home} onClick={onHomeContainerClick}>
          <i className={styles.home1}>HOME</i>
        </div>
        <div className={styles.frameContainer}>
          <i className={styles.stockPrediction}>Stock Prediction</i>
        </div>
        <div className={styles.aboutUs} onClick={onAboutUsContainerClick}>
          <i className={styles.aboutUs1}>About Us</i>
        </div>
      </div>

      <div className={styles.selectContainer}>
        <div className={styles.selectBlock}>
          <label className={styles.selectLabel}>Stock</label>
          <Select
            className="basic-single"
            classNamePrefix="select"
            defaultValue={companyOptions[0]}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isClearable={isClearable}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="color"
            options={companyOptions}
          />
          
        </div>

        <div className={styles.selectBlock}>
          <label className={styles.selectLabel}>Period</label>
          <Select
            className="basic-single"
            classNamePrefix="select"
            defaultValue={periodOptions[0]}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isClearable={isClearable}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="color"
            options={periodOptions}
          />
        </div>

        <div className={styles.selectBlock}>
          <label className={styles.selectLabel}>Interval</label>
          <Select
            className="basic-single"
            classNamePrefix="select"
            defaultValue={intervalOptions[0]}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isClearable={isClearable}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="color"
            options={periodOptions}
          />
        </div>
      </div>

      
      <button className={styles.predictBtn} onClick={handlePredictClick}>
        Predict
      </button>
      

      {/* <div className={styles.chart}>
        <AdvancedRealTimeChart theme="light" autosize />
      </div> */}
    </div>
  );
};

export default Prediction;
