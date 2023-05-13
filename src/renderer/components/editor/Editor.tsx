import React, {memo, useEffect} from "react";
import { Box, Text } from "@chakra-ui/react";
import SplitPane from "react-split-pane";
import { useDispatch, useSelector } from "react-redux";
import { getShowCode, getShowLayout } from "../../core/selectors/app";
import { useDropComponent } from "../../hooks/useDropComponent";
import ComponentPreview from "./ComponentPreview";
import CodePanel from "../CodePanel";
import { getComponents } from "../../core/selectors/components";
import {AppDispatch, RootState} from "../../redux/store";
import { unselect } from "../../redux/slices/uiBuilderComponentsSlice";
import log from "electron-log";
import { IComponent, IComponents } from "../../../react-app-env";
import { NodesState } from "../../redux/slices/machinesNodesSlice";

export const gridStyles = {
  // backgroundImage:
  //   'linear-gradient(to right, #d9e2e9 1px, transparent 1px),linear-gradient(to bottom, #d9e2e9 1px, transparent 1px);',
  // backgroundSize: '20px 20px',
  bgColor: "#0b0f14",
  p: 10
};
const Editor: React.FC = () => {
  // todo: have some props come in here?
  const dispatch = useDispatch<AppDispatch>();
  const showCode = useSelector(getShowCode);
  const showLayout = useSelector(getShowLayout);
  const components = useSelector(getComponents);
  const machinesComponents = useSelector((state: RootState) => state.nodes);

  const machines = convertNodesStateToIComponents(machinesComponents);
  const final_components = mergeIComponents(components, machines);

  useEffect(() => {
    console.log(final_components)
  }, [final_components])
  useEffect(() => {
    log.info("machinesComponents: ", machinesComponents)
  }, [machinesComponents])

  // todo: convert machineComponents to IComponents with component parent root



  const { drop } = useDropComponent("root");
  const isEmpty = !components.root.children.length;
  const rootProps = components.root.props;

  let editorBackgroundProps = {};

  const onSelectBackground = () => {
    dispatch(unselect());
  };

  if (showLayout) {
    editorBackgroundProps = gridStyles;
  }

  editorBackgroundProps = {
    ...editorBackgroundProps,
    ...rootProps
  };

  const Playground = (
    <Box
      p={2}
      {...editorBackgroundProps}
      height="100%"
      minWidth="10rem"
      width="100%"
      display={isEmpty ? "flex" : "block"}
      justifyContent="center"
      alignItems="center"
      overflow="auto"
      position="relative"
      ref={drop}
      flexDirection="column"
      onClick={onSelectBackground}
    >
      {final_components.root.children.map((name: string) => (
        <ComponentPreview key={name} componentName={name} />
      ))}
    </Box>
  );

  if (!showCode) {
    return Playground;

  }

  return (
    // @ts-ignore
    <SplitPane
      style={{ overflow: "auto" }}
      defaultSize="50%"
      resizerStyle={{
        border: "3px solid rgba(1, 22, 39, 0.21)",
        zIndex: 20,
        cursor: "row-resize"
      }}
      split="horizontal"
    >
      {Playground}
      <CodePanel />
    </SplitPane>
  );
};

export default memo(Editor);

const convertNodesStateToIComponents = (nodesState: NodesState): IComponents => {
  const components: IComponents = {};

  nodesState.outputNodes.forEach((node) => {
    const component: IComponent = {
      id: node.id+"-output"+node.outputId,
      type: "ChatComponent",
      parent: "root", // Set appropriate parent or root component ID
      children: [], // Set children if any, otherwise leave empty array
      props: {
        label: node.label,
        outputId: node.outputId,
        schemaId: node.schemaId,
        ui_message_registry: node.ui_message_registry,
      },
    };

    components[node.id] = component;
  });

  return components;
};

const mergeIComponents = (baseComponents: IComponents, componentsToAdd: IComponents): IComponents => {
  // Create a shallow copy of the baseComponents object
  const mergedComponents: IComponents = { ...baseComponents };

  // Create a new root component with a new children array
  const rootComponent = mergedComponents["root"];
  const newRootComponent: IComponent = {
    ...rootComponent,
    children: [...rootComponent.children],
  };
  mergedComponents["root"] = newRootComponent;

  // Iterate through componentsToAdd and add them as children to the root component of baseComponents
  for (const id in componentsToAdd) {
    const componentToAdd = componentsToAdd[id];

    // Add the component to the mergedComponents
    mergedComponents[id] = componentToAdd;

    // If the componentToAdd has a parent, skip adding it as a child
    if (componentToAdd.parent) continue;

    // Add the componentToAdd as a child to the new root component
    newRootComponent.children.push(id);
  }

  return mergedComponents;
};
