/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Heart3 } from "../../icons/Heart3";
import "./style.css";

export const Icon = ({
  icon,
  className,
  home = "/img/home-4.svg",
  union = "/img/union-6.svg",
  divClassName,
  img = "/img/union-10.svg",
  user = "/img/user-4.svg",
  frameClassName,
}) => {
  return (
    <div className={`icon ${className}`}>
      {["HOME", "MY"].includes(icon) && <img className="img" alt="Home" src={icon === "MY" ? user : home} />}

      {icon === "FAVORITE" && <Heart3 className="heart-3" />}

      {["FAVORITE", "HOME", "MY"].includes(icon) && (
        <div className="div">
          <div className={`HOME-2 ${icon} ${frameClassName}`}>
            {icon === "HOME" && <>HOME</>}

            {icon === "MY" && <>MY</>}

            {icon === "FAVORITE" && <>FAVORITE</>}
          </div>
        </div>
      )}

      {["SAVED", "SEARCH"].includes(icon) && (
        <>
          <div className={`flag icon-${icon}`}>
            {icon === "SAVED" && <img className="union-2" alt="Union" src={img} />}

            {icon === "SEARCH" && (
              <div className="frame">
                <img className="union-3" alt="Union" src={union} />
              </div>
            )}
          </div>
          <div className="div">
            <div className={`SAVED-2 icon-0-${icon} ${frameClassName}`}>
              {icon === "SAVED" && <>SAVED</>}

              {icon === "SEARCH" && <div className={`text-wrapper-2 ${divClassName}`}>SEARCH</div>}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

Icon.propTypes = {
  icon: PropTypes.oneOf(["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"]),
  home: PropTypes.string,
  union: PropTypes.string,
  img: PropTypes.string,
  user: PropTypes.string,
};
