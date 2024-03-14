/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const ButtonAi = ({ stateProp, className }) => {
  const [state, dispatch] = useReducer(reducer, {
    state: stateProp || "off",
  });

  return (
    <Link
      className={`button-AI state-3-${state.state} ${className}`}
      to="/result-2"
      onMouseLeave={() => {
        dispatch("mouse_leave");
      }}
      onMouseEnter={() => {
        dispatch("mouse_enter");
      }}
    >
      <div className="text-wrapper-7">AI 분석하기</div>
    </Link>
  );
};

function reducer(state, action) {
  switch (action) {
    case "mouse_enter":
      return {
        ...state,
        state: "on",
      };

    case "mouse_leave":
      return {
        ...state,
        state: "off",
      };
  }

  return state;
}

ButtonAi.propTypes = {
  stateProp: PropTypes.oneOf(["off", "on"]),
};
