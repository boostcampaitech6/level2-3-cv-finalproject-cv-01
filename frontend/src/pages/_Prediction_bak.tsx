import React, { FunctionComponent, useCallback, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import styles from './Prediction.module.css';
import { companyOptions, periodOptions, intervalOptionsMap } from '../docs/prediction_data';

const Prediction: FunctionComponent = () => {
  const navigate = useNavigate();

  const [selectedStock, setSelectedStock] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<string | null>(null);
  const [selectedInterval, setSelectedInterval] = useState<string | null>(null);
  const [intervalOptions, setIntervalOptions] = useState<{ label: string, value: string }[]>([]);

  

  // 출력값을 저장할 state
  const [predictionResult, setPredictionResult] = useState<string>('');

  useEffect(() => {
    if (selectedPeriod) {
      const options = intervalOptionsMap[selectedPeriod as keyof typeof intervalOptionsMap];
      if (options) {
        const newIntervalOptions = options.map(interval => ({
          label: interval, value: interval
        }));
        setIntervalOptions(newIntervalOptions);
        setSelectedInterval(newIntervalOptions[0].value);
      }
    } else {
      // 선택된 period가 없다면 interval 선택지를 비웁니다.
      setIntervalOptions([]);
      setSelectedInterval(null);

    }
  }, [selectedPeriod]);

  const onHomeContainerClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onAboutUsContainerClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);


  const handlePredictClick = () => {
    // 선택된 값들을 결과 상태에 저장합니다.
    const result = `Stock: ${selectedStock}, Period: ${selectedPeriod}, Interval: ${selectedInterval}`;
    setPredictionResult(result);
  };



  // const handlePredictClick = () => {
  //   console.log("Predict button clicked");
  // };

  const [isClearable, setIsClearable] = useState(true);
  const [isSearchable, setIsSearchable] = useState(true);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRtl, setIsRtl] = useState(false);

  return (
    <div className={styles.prediction}>
      <div className={styles.menuBar}>
        <div className={styles.home} onClick={onHomeContainerClick}>
          HOME
        </div>
        <div className={styles.frameContainer}>
          Stock Prediction
        </div>
        <div className={styles.aboutUs} onClick={onAboutUsContainerClick}>
          About Us
        </div>
      </div>

      <div className={styles.selectContainer}>
        <div className={styles.selectBlock}>
          <label className={styles.selectLabel}>Stock</label>
          <Select
            className="basic-single"
            classNamePrefix="select"
            value={selectedStock ? companyOptions.find(option => option.value === selectedStock) : null}
            onChange={(option) => setSelectedStock(option?.value || null)}
            options={companyOptions}
            placeholder="Select..."
            isClearable={isClearable}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="stock"
          />
        </div>

        <div className={styles.selectBlock}>
          <label className={styles.selectLabel}>Period</label>
          <Select
            className="basic-single"
            classNamePrefix="select"
            value={selectedPeriod ? periodOptions.find(option => option.value === selectedPeriod) : null}
            onChange={(option) => setSelectedPeriod(option?.value || null)}
            options={periodOptions}
            placeholder="Select..."
            isClearable={isClearable}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="period"
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
            name="interval"
            options={intervalOptions}
          />
        </div>
      </div>

      <button className={styles.predictBtn} onClick={handlePredictClick}>
        Predict
      </button>
      {/* 예측 결과를 보여주는 부분입니다. */}
      <div className={styles.predictionResult}>
        {predictionResult}
      </div>
    </div>
  );
};

export default Prediction;
