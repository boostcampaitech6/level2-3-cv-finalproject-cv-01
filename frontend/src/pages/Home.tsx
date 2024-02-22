import { FunctionComponent, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import FRAMERectangleSTOCK from "../components/FRAMERectangleSTOCK";
import styles from "./Home.module.css";

const Home: FunctionComponent = () => {
  const navigate = useNavigate();

  const onStockPredictionContainerClick = useCallback(() => {
    navigate("/prediction");
  }, [navigate]);

  const onAboutUsContainerClick = useCallback(() => {
    navigate("/about-us");
  }, [navigate]);

  return (
    <div className={styles.home}>
      <header className={styles.stockFrame}>
        <div className={styles.cNNModelForStockPredicti}>
          <div className={styles.predictionMenuBar}>
            <i className={styles.home1}>HOME</i>
          </div>
          <div
            className={styles.stockPrediction}
            onClick={onStockPredictionContainerClick}
          >
            <i className={styles.stockPrediction1}>Stock Prediction</i>
          </div>
          <div className={styles.aboutUs} onClick={onAboutUsContainerClick}>
            <i className={styles.aboutUs1}>About Us</i>
          </div>
        </div>
      </header>
      <main className={styles.nextGenerationAIStockPred}>
        <div className={styles.aboutUsFrame}>
          <h1 className={styles.theNextGenerationContainer}>
            <span>
              <p className={styles.theNextGeneration}>THE NEXT GENERATION</p>
              <p className={styles.aiStock}>AI STOCK PREDICTION</p>
            </span>
          </h1>
        </div>
        <FRAMERectangleSTOCK />
      </main>
      <footer className={styles.aiContainer}>
        <span className={styles.aiContainer1}>
          <p className={styles.ai}>{`AI 기술로 `}</p>
          <p className={styles.p}>증권 시장의 미래를</p>
          <p className={styles.p1}>예측합니다</p>
        </span>
      </footer>
      <img className={styles.image46Icon} alt="" src="/image-46@2x.png" />
      <div className={styles.div}>
        주식 시장은 방대한 양의 데이터와 복잡한 비선형적 특성을 가지고 있습니다.
        이러한 다이내믹한 데이터를 정확히 분석하고 모델링하기 위해서는 숨겨진
        패턴과 시장의 기본 원리를 효과적으로 파악할 수 있는 최적화된 기술이
        필요합니다.
      </div>
      <div className={styles.cnn}>
        시각적 데이터에서 특징을 추출하고 학습하는 CNN의 능력을 활용하여, 주식
        시장의 미묘한 변화와 숨겨진 패턴을 보다 정밀하게 포착할 수 있습니다.
        이를 통해 보다 정확하고 신뢰할 수 있는 주가 예측을 제공하고자 합니다.
      </div>
      <h1 className={styles.imageBasedDeepLearningContainer}>
        <span className={styles.imageBasedDeepLearningContainer1}>
          <p className={styles.imageBased}>{`Image-based `}</p>
          <p className={styles.deepLearning}>Deep Learning</p>
          <p className={styles.stockPrediction2}>Stock Prediction</p>
        </span>
      </h1>
      <img className={styles.image47Icon} alt="" src="/image-47@2x.png" />
      <h1 className={styles.disclaimer}>Disclaimer</h1>
      <div className={styles.div1}>
        모든 데이터와 정보는 정보 제공 목적으로만 제공됩니다. 그 어떤 데이터와
        정보도 일반적인 자문이나 맞춤형 자문 같은 투자 자문으로 간주되지
        않습니다. 모델의 예측 결과는 여러분의 투자 형태와 투자 목적 또는
        기대치에 적합하지 않을 수 있습니다.
      </div>
      <h1 className={styles.howTo}>How to</h1>
      <div className={styles.predictionContainer}>
        <ol className={styles.predictionChooseA}>
          <li className={styles.prediction}>
            메뉴바에서 Prediction을 눌러주세요. ✋
          </li>
          <li className={styles.chooseAStock}>
            Choose a stock에서 미래 주가가 궁금한 종목을 선택해 주세요. 🧑‍💻
          </li>
          <li className={styles.li}>
            조회하고 싶은 기간과 간격을 설정해 주세요. 🗓️
          </li>
          <li className={styles.prediction1}>
            이제 Prediction 버튼만 누르면 우리 모델이 열심히 예측할 거에요! 👀
          </li>
          <li>
            추가적으로 Candle matching을 누르면 캔들 매칭을 통한 정보도 확인
            가능해요! 😎
          </li>
        </ol>
      </div>
    </div>
  );
};

export default Home;
