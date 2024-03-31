/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { BasesIconWrapper } from "../BasesIconWrapper";
import "./style.css";

export const PropertyWrapper = ({ property1, className, basesIconWrapperColorClassName }) => {
  const [state, dispatch] = useReducer(reducer, {
    property1: property1 || "two",
  });

  return (
    <div
      className={`property-wrapper ${className}`}
      onClick={() => {
        dispatch("click");
      }}
    >
      <div className={`thumb property-1-${state.property1}`}>
        <BasesIconWrapper
          className={`${state.property1 === "two" ? "class-2" : "class-3"}`}
          color={state.property1 === "two" ? "/img/color-1.png" : "/img/color.svg"}
          colorClassName={basesIconWrapperColorClassName}
        />
      </div>
    </div>
  );
};

function reducer(state, action) {
  if (state.property1 === "one") {
    switch (action) {
      case "click":
        return {
          property1: "two",
        };
    }
  }

  if (state.property1 === "two") {
    switch (action) {
      case "click":
        return {
          property1: "one",
        };
    }
  }

  return state;
}

PropertyWrapper.propTypes = {
  property1: PropTypes.oneOf(["two", "one"]),
};
