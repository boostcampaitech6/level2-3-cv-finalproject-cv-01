import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Desktop.module.css";

const Desktop = () => {
  const navigate = useNavigate();

  const onPredictionTextClick = useCallback(() => {
    navigate("/desktop-2");
  }, [navigate]);

  const onTextClick = useCallback(() => {
    navigate("/desktop-2");
  }, [navigate]);

  return (
    <div className={styles.desktop1}>
      <div className={styles.ai}>
        <span>알려</span>
        <span className={styles.span}>주가</span>
        <span className={styles.ai1}>AI</span>
      </div>
      <div className={styles.market}>Market</div>
      <div className={styles.prediction} onClick={onPredictionTextClick}>
        Prediction
      </div>
      <div className={styles.game}>Game</div>
      <div className={styles.aboutUs}>About us</div>
      <div className={styles.login}>Login</div>
      <img className={styles.coinIcon} alt="" src="/coin.svg" />
      <img className={styles.desktop1Child} alt="" src="/group-1.svg" />
      <div className={styles.ai2}>- 쉽고 간편한 AI 주가 예측 서비스</div>
      <div className={styles.coinParent}>
        <img className={styles.coinIcon1} alt="" src="/coin.svg" />
        <div className={styles.ai3}>
          <p className={styles.p}>알려</p>
          <p className={styles.ai4}>
            <span>주가</span>
            <span className={styles.ai1}>AI</span>
          </p>
        </div>
      </div>
      <div className={styles.parent}>
        <b className={styles.b}>투자의 달인이 되어보세요!</b>
        <b className={styles.b1}>지금,</b>
      </div>
      <div className={styles.cnnParent}>
        <div className={styles.cnnContainer}>
          <p className={styles.p}>
            이미지 인식과 처리 분야에서 뛰어난 성능을 보이는 CNN 기술을 활용하여
            미래의 주가 움직임을 예측합니다.
          </p>
          <p className={styles.p}>&nbsp;</p>
          <p className={styles.p}>
            과거 주식 가격 변동을 이미지로 변환하고, 이 이미지 속 숨은 패턴과
            추세를 CNN 모델이 감지하고 주가를 예측합니다.
          </p>
          <p className={styles.p}>&nbsp;</p>
          <p className={styles.p}>
            이 모든 과정은 자동화 되어 수준 높은 주가 예측 결과를 얻을 수
            있습니다!
          </p>
        </div>
        <b className={styles.b2}>특별한 인공지능 기술</b>
        <b className={styles.b3}>✨ 이미지를 활용한 주가 예측 ✨</b>
        <div className={styles.aiParent}>
          <div className={styles.ai6}>
            <span>알려</span>
            <span className={styles.span}>주가</span>
            <span className={styles.ai7}>AI</span>
          </div>
          <b className={styles.b4}>만의</b>
        </div>
        <img className={styles.image6Icon} alt="" src="/image-6@2x.png" />
      </div>
      <div className={styles.group}>
        <b className={styles.b5}>이용방법</b>
        <div className={styles.ai8}>
          <span>알려</span>
          <span className={styles.span}>주가</span>
          <span className={styles.ai7}>AI</span>
        </div>
        <div className={styles.groupChild} />
        <b className={styles.b6}>사용법 간단하게 애니메이션</b>
      </div>
      <div className={styles.container}>
        <b className={styles.b7}>{`이제                          와 함께 `}</b>
        <b className={styles.b8}>주식 투자의 달인이 되어볼까요?!</b>
        <b className={styles.b9}>준비되셨나요?</b>
        <div className={styles.ai10}>
          <span>알려</span>
          <span className={styles.span}>주가</span>
          <span className={styles.ai7}>AI</span>
        </div>
      </div>
      <div className={styles.desktop1Item} />
      <b className={styles.b10} onClick={onTextClick}>
        예측하러 가기
      </b>
    </div>
  );
};

export default Desktop;
