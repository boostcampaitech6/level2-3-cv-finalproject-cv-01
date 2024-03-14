/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const Icon = ({
  icon,
  className,
  home = "/img/home-3.png",
  heart = "/img/heart-3.png",
  union = "/img/union-7.png",
  img = "/img/union-6.png",
  user = "/img/user-3.png",
  frameClassName,
  divClassName,
}) => {
  return (
    <div className={`icon ${icon} ${className}`}>
      {["FAVORITE", "HOME", "MY"].includes(icon) && (
        <img className="img" alt="Home" src={icon === "FAVORITE" ? heart : icon === "MY" ? user : home} />
      )}

      {["SAVED", "SEARCH"].includes(icon) && (
        <div className="flag">
          {icon === "SAVED" && <img className="union" alt="Union" src={img} />}

          {icon === "SEARCH" && (
            <div className="frame">
              <img className="union-2" alt="Union" src={union} />
            </div>
          )}
        </div>
      )}

      <div className="text-HOME">
        <div className={`div ${frameClassName}`}>
          {icon === "HOME" && <>HOME</>}

          {icon === "FAVORITE" && <>FAVORITE</>}

          {icon === "MY" && <>MY</>}

          {icon === "SAVED" && <>SAVED</>}

          {icon === "SEARCH" && <div className={`text-wrapper-2 ${divClassName}`}>SEARCH</div>}
        </div>
      </div>
    </div>
  );
};

Icon.propTypes = {
  icon: PropTypes.oneOf(["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"]),
  home: PropTypes.string,
  heart: PropTypes.string,
  union: PropTypes.string,
  img: PropTypes.string,
  user: PropTypes.string,
};
