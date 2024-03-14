import { PropertyOffWrapper } from ".";

export default {
  title: "Components/PropertyOffWrapper",
  component: PropertyOffWrapper,
  argTypes: {
    property1: {
      options: ["off", "on"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    property1: "off",
    propertyOffClassName: {},
  },
};
