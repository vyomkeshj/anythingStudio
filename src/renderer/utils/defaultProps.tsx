import React from "react";
import * as Chakra from "@chakra-ui/react";
import {
  AspectRatioProps,
  BoxProps,
  ButtonProps,
  CenterProps,
  ContainerProps,
  DividerProps,
  FlexProps,
  GridProps,
  HeadingProps,
  IconProps,
  ImageProps,
  InputProps,
  SelectProps,
  SwitchProps,
  TabListProps,
  TabPanelProps,
  TabPanelsProps,
  TabProps,
  TabsProps
} from "@chakra-ui/react";
import iconsList from "../iconsList";
import { ComponentType } from "../../react-app-env";


type PropsWithForm<T> = T & { form?: T }

type PreviewDefaultProps = {
  Box?: PropsWithForm<BoxProps>
  Button?: PropsWithForm<ButtonProps>
  Icon?: PropsWithForm<IconProps> & { icon: keyof typeof iconsList }
  Image?: PropsWithForm<ImageProps>
  Divider?: PropsWithForm<DividerProps>
  Heading?: PropsWithForm<HeadingProps>
  Switch?: PropsWithForm<SwitchProps>
  Flex?: PropsWithForm<FlexProps>
  Grid?: PropsWithForm<GridProps>
  TabList?: PropsWithForm<TabListProps>
  TabPanel?: PropsWithForm<TabPanelProps>
  TabPanels?: PropsWithForm<TabPanelsProps>
  Tab?: PropsWithForm<TabProps>
  Tabs?: PropsWithForm<TabsProps>
  Select?: PropsWithForm<SelectProps & { children: JSX.Element }>
  Input?: PropsWithForm<InputProps>
  AspectRatio?: PropsWithForm<AspectRatioProps>
  Center?: PropsWithForm<CenterProps>
  Container?: PropsWithForm<ContainerProps>
}

export const DEFAULT_PROPS: PreviewDefaultProps = {
  Divider: { borderColor: "blackAlpha.500" },
  Flex: {
    form: {
      display: "flex"
    }
  },
  Grid: {
    templateColumns: "repeat(5, 1fr)",
    gap: 6,
    form: {
      display: "grid"
    }
  },
  Heading: {
    children: "Heading title"
  },
  Icon: { icon: "CopyIcon" },
  Image: {
    height: "100px",
    width: "100px"
  },
  Switch: {
    isChecked: false
  },
  Tab: { children: "Tab" },
  Tabs: { children: "", size: "md" },
  TabPanel: { children: "Tab" },
};

export const getDefaultFormProps = (type: ComponentType) => {
  //@ts-ignore
  const chakraDefaultProps = Chakra[type].defaultProps;
  // @ts-ignore
  return { ...chakraDefaultProps, ...DEFAULT_PROPS[type]?.form };
};
