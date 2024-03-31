/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/


import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const Heart = ({ stateProp, className, onClick }) => {
  const handleClick = (event) => {
    event.stopPropagation(); // 이벤트 전파를 중단합니다.
    if (onClick) onClick(event); // 부모 컴포넌트에서 전달된 onClick 핸들러에 이벤트 객체를 전달합니다.
  };

  return (
    <div
      className={`heart ${stateProp} ${className}`}
      onClick={handleClick}
    />
  );
};

Heart.propTypes = {
  stateProp: PropTypes.oneOf(["off", "on"]),
};



// import PropTypes from "prop-types";
// import React, { useState } from 'react';
// import { Heart } from "./Heart"
// import "./style.css";

// export const Heart = ({ stateProp, className, onClick }) => {
//   const [state, dispatch] = useReducer(reducer, {
//     state: stateProp || "off",
//   });

//   const handleClick = (event) => {
//     event.stopPropagation();
//     dispatch({ type: 'TOGGLE_HEART' }); // 액션을 dispatch합니다.
//     if (onClick) onClick(event); // 추가적인 부모 컴포넌트의 핸들러가 있을 경우 호출합니다.
//   };

//   return (
//     <div
//       className={`heart ${state.state} ${className}`}
//       onClick={handleClick} // 수정된 핸들러를 사용합니다.
//     />
//   );
// };

// // 상태를 토글하는 reducer 함수
// function reducer(state, action) {
//   switch (action.type) {
//     case 'TOGGLE_HEART':
//       return {
//         ...state,
//         state: state.state === 'off' ? 'on' : 'off',
//       };
//     default:
//       return state;
//   }
// }

// Heart.propTypes = {
//   stateProp: PropTypes.oneOf(["off", "on"]),
// };


