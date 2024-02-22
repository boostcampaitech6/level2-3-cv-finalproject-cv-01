import { FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Prediction.module.css";

const Prediction: FunctionComponent = () => {
  const navigate = useNavigate();

  const onHomeContainerClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onAboutUsContainerClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);

  return (
    <div className={styles.prediction}>
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
  );
};

export default Prediction;
