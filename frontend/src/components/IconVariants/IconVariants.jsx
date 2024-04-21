/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Icon } from "../Icon";
import "./style.css";

export const IconVariants = ({
  icon,
  state,
  className,
  iconHome = "/img/home-1.svg",
  iconUnion = "/img/union-1.svg",
  iconUser = "/img/user-1.svg",
  to,
}) => {

  const isFavoriteOn = icon === "FAVORITE" && state === "on";

  return (
    <Link className={`icon-variants ${className}`} to={to}>
      <Icon
        className="icon-instance"
        isFavoriteOn={isFavoriteOn}
        divClassName={`${state === "on" && icon === "SEARCH" && "class"}`}
        frameClassName={`${
          ((icon === "FAVORITE" && state === "on") ||
            (icon === "HOME" && state === "on") ||
            (icon === "MY" && state === "on") ||
            (icon === "SAVED" && state === "on")) &&
          "class"
        }`}
        home={iconHome}
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
            ? "/img/union.svg"
            : state === "on" && icon === "SEARCH"
            ? "/img/union-3.svg"
            : undefined
        }
        user={iconUser}
      />
    </Link>
  );
};

IconVariants.propTypes = {
  icon: PropTypes.oneOf(["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"]),
  state: PropTypes.oneOf(["off", "on"]),
  iconHome: PropTypes.string,
  iconUnion: PropTypes.string,
  iconUser: PropTypes.string,
  to: PropTypes.string,
};
