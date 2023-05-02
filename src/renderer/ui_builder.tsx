import React, { memo } from "react";
import { Flex, Box } from '@chakra-ui/react'
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { Global } from '@emotion/react'
import useShortcuts from "./hooks/useShortcuts";
import Sidebar from "./components/sidebar/Sidebar";
import Editor from "./components/editor/Editor";
import Metadata from "./components/Metadata";
import EditorErrorBoundary from "./components/errorBoundaries/EditorErrorBoundary";
import { InspectorProvider } from "./contexts/inspector-context";
import Inspector from "./components/inspector/Inspector";
import { Header } from "./components/Header/Header";

const UIBuilder = memo(() => {
  useShortcuts()

  return (
    <>
      <Global
        styles={() => ({
          html: { minWidth: '860px', backgroundColor: '#1a202c' },
        })}
      />
      <Metadata />
      <Header />
      {/*<DndProvider backend={HTML5Backend}>*/}
        <Flex h="calc(100vh - 3rem)">
          <Sidebar />
          <EditorErrorBoundary>
            <Box bg="white" flex={1} position="relative">
              <Editor />
            </Box>
          </EditorErrorBoundary>

          <Box
            maxH="calc(100vh - 3rem)"
            flex="0 0 15rem"
            bg="#f7fafc"
            overflowY="auto"
            overflowX="visible"
            borderLeft="1px solid #cad5de"
          >
            <InspectorProvider>
              <Inspector />
            </InspectorProvider>
          </Box>
        </Flex>
      {/*</DndProvider>*/}
    </>
  )
})


export default UIBuilder
