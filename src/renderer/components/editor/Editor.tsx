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

export const gridStyles = {
  // backgroundImage:
  //   'linear-gradient(to right, #d9e2e9 1px, transparent 1px),linear-gradient(to bottom, #d9e2e9 1px, transparent 1px);',
  // backgroundSize: '20px 20px',
  bgColor: "#0b0f14",
  p: 10
};
/*export interface MachinesNodeUI {
    id: string;
    type: ExpressionJson;
    neverReason?: string | null;
    label: string;
    kind: OutputKind;
    ui_message_registry: OutputChannel[];
    outputId: OutputId;
    useOutputData: Function;
    schemaId: string;
    definitionType: Type;
    hasHandle: boolean;
    animated: undefined | boolean;
    jsx: JSX.Element;
}
*/

/*
export interface IComponent {
  children: string[]
  type: ComponentType
  parent: string
  id: string
  props: any
  rootParentType?: ComponentType
  componentName?: string
}
 */
const Editor: React.FC = () => {
  // todo: have some props come in here?
  const dispatch = useDispatch<AppDispatch>();
  const showCode = useSelector(getShowCode);
  const showLayout = useSelector(getShowLayout);
  const components = useSelector(getComponents);
  const machinesComponents = useSelector((state: RootState) => state.nodes);

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
      {components.root.children.map((name: string) => (
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
