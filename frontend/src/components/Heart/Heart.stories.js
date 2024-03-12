import { Heart } from ".";

export default {
  title: "Components/Heart",
  component: Heart,
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
