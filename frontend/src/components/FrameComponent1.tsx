import { FunctionComponent } from "react";
import styles from "./FrameComponent1.module.css";

const FrameComponent1: FunctionComponent = () => {
  return (
    <section className={styles.aboutUsInner}>
      <div className={styles.aboutUsParent}>
        <h1 className={styles.aboutUs}>About us</h1>
        <div className={styles.aiTech6Parent}>
          <i className={styles.aiTech6}>네이버 부스트캠프 AI Tech 6기</i>
          <i className={styles.cv01Team}>CV-01조 Team 내돈내산</i>
        </div>
      </div>
    </section>
  );
};

export default FrameComponent1;
