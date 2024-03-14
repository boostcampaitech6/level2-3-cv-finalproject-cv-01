import { ButtonAi } from ".";

export default {
  title: "Components/ButtonAi",
  component: ButtonAi,
  argTypes: {
    stateProp: {
      options: ["off", "on"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    stateProp: "off",
    className: {},
  },
};
