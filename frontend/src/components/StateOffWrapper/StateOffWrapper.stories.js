import { StateOffWrapper } from ".";

export default {
  title: "Components/StateOffWrapper",
  component: StateOffWrapper,
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
    text: "NAVER",
    text1: "035420",
    logoClassName: {},
  },
};
