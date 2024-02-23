import { FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import FrameComponent1 from "../components/FrameComponent1";
import FrameComponentGitub from "../components/FrameComponentGitub";
import styles from "./AboutUs.module.css";

const AboutUs: FunctionComponent = () => {
  const navigate = useNavigate();

  const onHomeContainerClick = useCallback(() => {
    navigate("/");
  }, [navigate]);

  const onStockPredictionContainerClick = useCallback(() => {
    navigate("/prediction");
  }, [navigate]);

  return (
    <div className={styles.aboutUs}>
      <header className={styles.fRAMEWrapper}>
        <div className={styles.fRAME}>
          <div className={styles.home} onClick={onHomeContainerClick}>
            <i className={styles.home1}>HOME</i>
          </div>
          <div className={styles.stockPredictionFrame}>
            <div
              className={styles.stockPrediction}
              onClick={onStockPredictionContainerClick}
            >
              <i className={styles.stockPrediction1}>Stock Prediction</i>
            </div>
          </div>
          <i className={styles.aboutUs1}>About Us</i>
        </div>
      </header>
      <FrameComponent1 />
      <div className={styles.aboutUsChild} />
      <FrameComponentGitub />
      <section className={styles.cnnContainer}>
        <span className={styles.cnnContainer1}>
          <p className={styles.p}>
            사용자들에게 새로운 활용 가능성과 즐거움을 제공하는 서비스 개발을
            목표로 모인 팀, 내돈내산입니다!
          </p>
          <p className={styles.p1}>
            우리는 일반적인 시계열 데이터 분석을 넘어 금융 데이터를 새로운
            시각으로 탐색하고자 합니다.
          </p>
          <p className={styles.blankLine}>&nbsp;</p>
          <p className={styles.p2}>
            기존의 금융 분석 방식에서 벗어나, 이미지로 변환된 주식 데이터를
            이용합니다.
          </p>
          <p className={styles.cnn}>
            이미지 데이터와 CNN 모델을 활용하면 주식 데이터를 시각적으로
            분석하고, 주가의 움직임을 보다 직관적으로 파악할 수 있습니다.
          </p>
          <p className={styles.blankLine1}>&nbsp;</p>
          <p className={styles.p3}>
            투자자들은 우리 서비스를 통해 더 시각적이고 직관적인 정보를
            제공받기에 시장에서 긍정적인 의사결정을 할 수 있습니다.
          </p>
        </span>
      </section>
      <div className={styles.boostcampAi6thCv01gmailc}>
        boostcamp_ai_6th_cv-01@gmail.com
      </div>
      <h1 className={styles.contactUs}>Contact us</h1>
    </div>
  );
};

export default AboutUs;
