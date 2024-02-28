import { FunctionComponent, useCallback } from "react";
import Component from "./Component";
import styles from "./FrameComponent.module.css";

const FrameComponent: FunctionComponent = () => {
  const onContainerClick = useCallback(() => {
    window.open("https://github.com/minyun-e");
  }, []);

  const onContainer1Click = useCallback(() => {
    window.open("https://github.com/2018007956");
  }, []);

  const onContainer2Click = useCallback(() => {
    window.open("https://github.com/Eddie-JUB/");
  }, []);

  const onContainer3Click = useCallback(() => {
    window.open("https://github.com/FinalCold");
  }, []);

  const onContainer4Click = useCallback(() => {
    window.open("https://github.com/MalMyeong");
  }, []);

  const onContainer5Click = useCallback(() => {
    window.open("https://github.com/classaen7");
  }, []);

  return (
    <section className={styles.profileFrame}>
      <div className={styles.profile}>
        <Component
          rectangle26="/rectangle-26@2x.png"
          prop="김민윤"
          onContainerClick={onContainerClick}
        />
        <Component
          rectangle26="/rectangle-26-1@2x.png"
          prop="김채아"
          onContainerClick={onContainer1Click}
        />
        <Component
          rectangle26="/rectangle-26-2@2x.png"
          prop="배종욱"
          onContainerClick={onContainer2Click}
        />
        <Component
          rectangle26="/rectangle-26-3@2x.png"
          prop="박찬종"
          onContainerClick={onContainer3Click}
        />
        <Component
          rectangle26="/rectangle-26-4@2x.png"
          prop="조명현"
          onContainerClick={onContainer4Click}
        />
        <Component
          rectangle26="/rectangle-26-5@2x.png"
          prop="최시현"
          onContainerClick={onContainer5Click}
        />
      </div>
    </section>
  );
};

export default FrameComponent;
