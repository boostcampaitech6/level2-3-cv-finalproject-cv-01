import { IconVariants } from ".";

export default {
  title: "Components/IconVariants",
  component: IconVariants,
  argTypes: {
    icon: {
      options: ["MY", "HOME", "FAVORITE", "SEARCH", "SAVED"],
      control: { type: "select" },
    },
    state: {
      options: ["off", "on"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    icon: "MY",
    state: "off",
    className: {},
    iconUnion: "/img/union-1.png",
  },
};
