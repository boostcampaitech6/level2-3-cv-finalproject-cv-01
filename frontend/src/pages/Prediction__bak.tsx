import { FunctionComponent, useCallback } from "react";
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import styles from "./Prediction.module.css";
import Select from 'react-select';
import FrameComponentStockPrediction from "../components/FrameComponentStockPrediction";
import FrameComponentGitub from "../components/FrameComponentSelection";
// import { colourOptions } from '../docs/data';
import { companyOptions, periodOptions, intervalOptions } from '../docs/prediction_data';


const Checkbox = ({ children, ...props }: JSX.IntrinsicElements['input']) => (
  <label style={{ marginRight: '1em' }}>
    <input type="checkbox" {...props} />
    {children}
  </label>
);

const PredictionWithSelect: React.FunctionComponent = () => {
  const navigate = useNavigate();
  const [isClearable, setIsClearable] = useState(true);
  const [isSearchable, setIsSearchable] = useState(true);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRtl, setIsRtl] = useState(false);

  const onHomeContainerClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onStockPredictionContainerClick = useCallback(() => {
    navigate("/prediction");
  }, [navigate]);

  const onAboutUsContainerClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);

  return (

    <div className={styles.prediction}>
      <header className={styles.fRAMEWrapper}>
        <div className={styles.home} onClick={onHomeContainerClick}>
          <i>HOME</i>
          {/* <i className={styles.home1}>HOME</i> */}
        </div>
        <div className={styles.frameContainer} onClick={onStockPredictionContainerClick}>
          <i>Stock Prediction</i>
          {/* <i className={styles.stockPrediction}>Stock Prediction</i> */}
        </div>
        <div className={styles.aboutUs} onClick={onAboutUsContainerClick}>
          <i>About Us</i>
          {/* <i className={styles.aboutUs1}>About Us</i> */}
        </div>
      </header>

      {/* <FrameComponent1 /> */}
      <div className={styles.stockPredictionChild} />
      {/* <FrameComponent /> */}
      <section className={styles.cnnContainer}>
        
      {/* Add Select components here */}
      <div className={styles.middle}>
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

      <div className={styles.middle}>
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

      <div className={styles.middle}>
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
          options={intervalOptions}
        />
      </div>


      </section>
      
    </div>
  );
};

export default PredictionWithSelect;
