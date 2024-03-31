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
    home: "/img/home-4.svg",
    union: "/img/union-6.svg",
    divClassName: {},
    img: "/img/union-10.svg",
    user: "/img/user-4.svg",
    frameClassName: {},
  },
};
