/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Icon } from "../Icon";
import "./style.css";

export const IconVariants = ({ icon, state, className, iconUnion = "/img/union-1.png", to }) => {
  return (
    <Link className={`icon-variants icon-1-${icon} state-1-${state} ${className}`} to={to}>
      <Icon
        className="icon-instance"
        divClassName={`${state === "on" && icon === "SEARCH" && "class"}`}
        frameClassName={`${
          ((icon === "FAVORITE" && state === "on") ||
            (icon === "HOME" && state === "on") ||
            (icon === "MY" && state === "on") ||
            (icon === "SAVED" && state === "on")) &&
          "class"
        }`}
        heart={
          state === "off" && icon === "FAVORITE"
            ? "/img/heart.png"
            : state === "on" && icon === "FAVORITE"
            ? "/img/heart-2.png"
            : undefined
        }
        home={
          state === "off" && icon === "HOME"
            ? "/img/home.png"
            : state === "on" && icon === "HOME"
            ? "/img/home-2.png"
            : undefined
        }
        icon={
          icon === "FAVORITE"
            ? "FAVORITE"
            : icon === "SEARCH"
            ? "SEARCH"
            : icon === "SAVED"
            ? "SAVED"
            : icon === "MY"
            ? "MY"
            : "HOME"
        }
        img={iconUnion}
        union={
          state === "off" && icon === "SEARCH"
            ? "/img/union.png"
            : state === "on" && icon === "SEARCH"
            ? "/img/union-3.png"
            : undefined
        }
        user={
          state === "off" && icon === "MY"
            ? "/img/user.png"
            : state === "on" && icon === "MY"
            ? "/img/user-2.png"
            : undefined
        }
      />
    </Link>
  );
};

IconVariants.propTypes = {
  icon: PropTypes.oneOf(["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"]),
  state: PropTypes.oneOf(["off", "on"]),
  iconUnion: PropTypes.string,
  to: PropTypes.string,
};
