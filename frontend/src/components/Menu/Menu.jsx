/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { IconVariants } from "../IconVariants";
import "./style.css";

export const Menu = ({
  className,
  iconVariantsIconHome = "/img/home.svg",
  iconVariantsState = "off",
  iconVariantsIconUnion = "/img/union-1.svg",
  iconVariantsState1 = "off",
  iconVariantsState2 = "off",
  iconVariantsIconUser = "/img/user.svg",
  iconVariantsState3 = "off",
  to,
  to1,
  to2,
  to3,
}) => {
  return (
    <div className={`menu ${className}`}>
      <IconVariants
        className="icon-variants-instance"
        icon="HOME"
        iconHome={iconVariantsIconHome}
        state={iconVariantsState1}
        to={to}
      />
      <IconVariants className="icon-variants-instance" icon="FAVORITE" state={iconVariantsState3} to={to1} />
      <IconVariants className="icon-variants-instance" icon="SEARCH" state={iconVariantsState} to={to3} />
      <IconVariants className="icon-variants-instance" icon="SAVED" iconUnion={iconVariantsIconUnion} state="off" />
      <IconVariants
        className="icon-variants-instance"
        icon="MY"
        iconUser={iconVariantsIconUser}
        state={iconVariantsState2}
        to={to2}
      />
    </div>
  );
};

Menu.propTypes = {
  iconVariantsIconHome: PropTypes.string,
  iconVariantsState: PropTypes.string,
  iconVariantsIconUnion: PropTypes.string,
  iconVariantsState1: PropTypes.string,
  iconVariantsState2: PropTypes.string,
  iconVariantsIconUser: PropTypes.string,
  iconVariantsState3: PropTypes.string,
  to: PropTypes.string,
  to1: PropTypes.string,
  to2: PropTypes.string,
  to3: PropTypes.string,
};
