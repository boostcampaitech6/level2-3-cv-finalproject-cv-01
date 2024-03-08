import { FunctionComponent } from "react";
import styles from "./Component.module.css";

export type ComponentType = {
  rectangle26?: string;
  prop?: string;

  /** Action props */
  onContainerClick?: () => void;
};

const Component: FunctionComponent<ComponentType> = ({
  rectangle26,
  prop,
  onContainerClick,
}) => {
  return (
    <div className={styles.div} onClick={onContainerClick}>
      <div className={styles.image}>
        <img
          className={styles.imageChild}
          loading="eager"
          alt=""
          src={rectangle26}
        />
      </div>
      <div className={styles.name}>
        <i className={styles.i}>{prop}</i>
      </div>
      <div className={styles.frame} />
    </div>
  );
};

export default Component;
