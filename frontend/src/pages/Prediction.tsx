import React, { FunctionComponent, useCallback, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import styles from './Prediction.module.css';
import { companyOptions, periodOptions, intervalOptionsMap } from '../docs/prediction_data';
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";

const Prediction: FunctionComponent = () => {
  const navigate = useNavigate();

  const [selectedStock, setSelectedStock] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<string | null>(null);
  const [selectedInterval, setSelectedInterval] = useState<string | null>(null);
  const [intervalOptions, setIntervalOptions] = useState<{ label: string, value: string }[]>([]);

  // 출력값을 저장할 state
  const [predictionResult, setPredictionResult] = useState<string>('');


  const handleIntervalChange = (option: { value: string; label: string } | null) => {
    setSelectedInterval(option ? option.value : null);
  };
  const [chartKey, setChartKey] = useState<string>("");

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

  // Predict 버튼 클릭 핸들러
  const handlePredictClick = () => {

    if (!selectedStock || !selectedPeriod || !selectedInterval) {
      const missingSelections = [];
      if (!selectedStock) missingSelections.push('Stock');
      if (!selectedPeriod) missingSelections.push('Period');
      if (!selectedInterval) missingSelections.push('Interval');
      setPredictionResult(`Please select ${missingSelections.join(', ')}`);
    } 
    else {
      setPredictionResult(`Stock: ${selectedStock}, Period: ${selectedPeriod}, Interval: ${selectedInterval}`);
      setShowChart(true);
      setChartKey(`${selectedStock}-${selectedPeriod}-${selectedInterval}-${new Date().getTime()}`);
      const periodForChart = convertPeriodToTradingViewFormat(selectedPeriod);
      const intervalForChart = convertIntervalToTradingViewFormat(selectedInterval);
    }
  };

  const [isClearable, setIsClearable] = useState(true);
  const [isSearchable, setIsSearchable] = useState(true);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRtl, setIsRtl] = useState(false);
  const [showChart, setShowChart] = useState(false); // 차트 표시 상태

  // 변환 함수 정의
  const convertIntervalToTradingViewFormat = (interval: string | null): "1" | "3" | "5" | "15" | "30" | "60" |"D" | "W" | undefined => {
    const mapping: { [key: string]: "1" | "3" | "5" | "15" | "30" | "60" |"D" | "W" } = {
      '1m': '1',
      '3m': '3',
      '5m': '5',
      '15m': '15',
      '30m': '30',
      '60m': '60',
      '1d': 'D',
      '1w': 'W',
      // 매핑이 필요한 다른 간격을 추가합니다.
    };
    return interval ? mapping[interval] : undefined;
  };
 
  const convertPeriodToTradingViewFormat = (period: string | null): "1D" | "5D" | "1M" | "3M" | "6M" |"12M" | "YTD"  | "60M" | "ALL" | undefined => {
    const mapping: { [key: string]: "1D" | "5D" | "1M" | "3M" | "6M" | "YTD" | "12M" | "60M" | "ALL" } = {
      '1d': '1D',
      '5d': '5D',
      '1mo': '1M',
      '3mo': '3M',
      '6mo': '6M',
      '1y': '12M',
      '2y': 'ALL', // "2Y"와 그 이상은 "ALL"로 변경
      '5y': 'ALL',
      '10y': 'ALL',
    };
    return period ? mapping[period] : undefined;
  };


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
            value={selectedInterval ? intervalOptions.find(option => option.value === selectedInterval) : null}
            onChange={(option) => setSelectedInterval(option?.value || null)}
            options={intervalOptions}
            placeholder="Select..."
            isClearable={isClearable}
            isDisabled={isDisabled}
            isLoading={isLoading}
            isRtl={isRtl}
            isSearchable={isSearchable}
            name="interval"
          />
        </div>

      </div>

      <button className={styles.predictBtn} onClick={handlePredictClick}>
        Predict
      </button>

      <div className={styles.predictionResult}>
        {predictionResult}
      </div>

      {showChart && selectedStock && selectedInterval && (
        <div className={styles.chart}>
          <AdvancedRealTimeChart
            key={chartKey}
            theme="dark"
            symbol={selectedStock}
            range={convertPeriodToTradingViewFormat(selectedPeriod)}
            // interval='60'
            // interval={convertIntervalToTradingViewFormat(selectedInterval)}
            timezone="Asia/Seoul"
            style="1"
            locale="kr"
            withdateranges={true}
            toolbar_bg="#f1f3f6"
            allow_symbol_change={true}
            container_id={`tradingview_${chartKey}`}
            // allow_symbol_change={false}
            // container_id="tradingview_dcf24"
          />
        </div>
      )}

    </div>




  );
};

export default Prediction;
