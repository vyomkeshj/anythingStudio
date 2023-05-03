import React, { memo } from 'react'
import { Box, Text, Link } from '@chakra-ui/react'
import SplitPane from 'react-split-pane'
import { useSelector, useDispatch } from "react-redux";
import { getShowCode, getShowLayout } from "../../core/selectors/app";
import { useDropComponent } from "../../hooks/useDropComponent";
import ComponentPreview from "./ComponentPreview";
import CodePanel from "../CodePanel";
import { getComponents } from "../../core/selectors/components";
import {AppDispatch} from "../../redux/store";
import {loadDemo, unselect} from "../../redux/slices/uiBuilderComponentsSlice";

export const gridStyles = {
  // backgroundImage:
  //   'linear-gradient(to right, #d9e2e9 1px, transparent 1px),linear-gradient(to bottom, #d9e2e9 1px, transparent 1px);',
  // backgroundSize: '20px 20px',
  bgColor: '#0b0f14',
  p: 10,
}

const Editor: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const showCode = useSelector(getShowCode)
  const showLayout = useSelector(getShowLayout)
  const components = useSelector(getComponents)

  const { drop } = useDropComponent('root')
  const isEmpty = !components.root.children.length
  const rootProps = components.root.props

  let editorBackgroundProps = {}

  const onSelectBackground = () => {
    dispatch(unselect())
  }

  if (showLayout) {
    editorBackgroundProps = gridStyles
  }

  editorBackgroundProps = {
    ...editorBackgroundProps,
    ...rootProps,
  }

  const Playground = (
    <Box
      p={2}
      {...editorBackgroundProps}
      height="100%"
      minWidth="10rem"
      width="100%"
      display={isEmpty ? 'flex' : 'block'}
      justifyContent="center"
      alignItems="center"
      overflow="auto"
      position="relative"
      ref={drop}
      flexDirection="column"
      onClick={onSelectBackground}
    >
      {isEmpty && (
        <Text maxWidth="md" color="gray.400" fontSize="xl" textAlign="center">
          Drag a component here
        </Text>
      )}

      {components.root.children.map((name: string) => (
        <ComponentPreview key={name} componentName={name} />
      ))}
    </Box>
  )

  if (!showCode) {
    return Playground

  }

  return (
    // @ts-ignore
    <SplitPane
      style={{ overflow: 'auto' }}
      defaultSize="50%"
      resizerStyle={{
        border: '3px solid rgba(1, 22, 39, 0.21)',
        zIndex: 20,
        cursor: 'row-resize',
      }}
      split="horizontal"
    >
      {Playground}
      <CodePanel />
    </SplitPane>
  )
}

export default memo(Editor)
