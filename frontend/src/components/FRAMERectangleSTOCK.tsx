import { FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./FRAMERectangleSTOCK.module.css";

const FRAMERectangleSTOCK: FunctionComponent = () => {
  const navigate = useNavigate();

  const onRectangleRectangleClick = useCallback(() => {
    navigate("/prediction");
  }, [navigate]);

  const onRectangleClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);

  return (
    <section className={styles.fRAMERectangleSTOCK}>
      <div className={styles.aboutUsFrameRectangle} />
      <div className={styles.sTOCKPREDICTION}>
        <div className={styles.frameFrame}>
          <div
            className={styles.rectangleRectangle}
            onClick={onRectangleRectangleClick}
          />
          <i className={styles.stockPrediction}>
            <span className={styles.stockPredictionTxtContainer}>
              <p className={styles.stock}>STOCK</p>
              <p className={styles.prediction}>PREDICTION</p>
            </span>
          </i>
        </div>
        <div className={styles.frameFrame1}>
          <div className={styles.frameFrameChild} onClick={onRectangleClick} />
          <i className={styles.aboutUs}>About Us</i>
        </div>
      </div>
    </section>
  );
};

export default FRAMERectangleSTOCK;
