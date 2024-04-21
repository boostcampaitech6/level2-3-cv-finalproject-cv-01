import { Loding } from ".";

export default {
  title: "Components/Loding",
  component: Loding,
  argTypes: {
    frame: {
      options: ["two", "one", "three", "four"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    frame: "two",
    className: {},
    ellipse: "/img/ellipse-2-3.svg",
  },
};
