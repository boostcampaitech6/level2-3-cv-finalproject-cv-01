import { Component1009 } from ".";

export default {
  title: "Components/Component1009",
  component: Component1009,
  argTypes: {
    state: {
      options: ["off", "on"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    state: "off",
    className: {},
    divClassName: {},
    text: "네이버",
    logoClassName: {},
  },
};
