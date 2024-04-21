import { PropertyWrapper } from ".";

export default {
  title: "Components/PropertyWrapper",
  component: PropertyWrapper,
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
    className: {},
    basesIconWrapperColorClassName: {},
  },
};
