import { Icon } from ".";

export default {
  title: "Components/Icon",
  component: Icon,
  argTypes: {
    icon: {
      options: ["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    icon: "MY",
    className: {},
    home: "/img/home-3.png",
    heart: "/img/heart-3.png",
    union: "/img/union-7.png",
    img: "/img/union-6.png",
    user: "/img/user-3.png",
    frameClassName: {},
    divClassName: {},
  },
};
