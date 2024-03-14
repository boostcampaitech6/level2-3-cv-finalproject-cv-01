/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { IconVariants } from "../IconVariants";
import "./style.css";

export const Menu = ({ className, iconVariantsIconUnion = "/img/union-1.png", to, to1, to2, to3 }) => {
  return (
    <div className={`menu ${className}`}>
      <IconVariants className="icon-variants-instance" icon="HOME" state="off" to={to} />
      <IconVariants className="icon-variants-instance" icon="FAVORITE" state="off" to={to1} />
      <IconVariants className="icon-variants-instance" icon="SEARCH" state="off" to={to2} />
      <IconVariants className="icon-variants-instance" icon="SAVED" iconUnion={iconVariantsIconUnion} state="off" />
      <IconVariants className="icon-variants-instance" icon="MY" state="off" to={to3} />
    </div>
  );
};

Menu.propTypes = {
  iconVariantsIconUnion: PropTypes.string,
  to: PropTypes.string,
  to1: PropTypes.string,
  to2: PropTypes.string,
  to3: PropTypes.string,
};
