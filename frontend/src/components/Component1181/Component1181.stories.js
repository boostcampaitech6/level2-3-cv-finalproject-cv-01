import { Component1181 } from ".";

export default {
  title: "Components/Component1181",
  component: Component1181,
  argTypes: {
    property1: {
      options: ["two", "one"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    property1: "two",
    basesIconWrapperColorClassName: {},
  },
};
