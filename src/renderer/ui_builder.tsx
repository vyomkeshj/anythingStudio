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
import HeaderUI from "./components/Header";
import { Header } from "./components/Header/Header";

const UIBuilder = memo(() => {
  // useShortcuts()

  return (
      <>
        <Global
            styles={() => ({
              html: { minWidth: '860px', backgroundColor: '#101631' },
            })}
        />
        <Metadata />
        {/*<Header />*/}
        <HeaderUI />
        <DndProvider backend={HTML5Backend}>
          <Flex h="calc(100vh - 3rem)">
            <Sidebar />
            <EditorErrorBoundary>
              <Box bg="#0c0e13" flex={1} position="relative">
                <Editor />
              </Box>
            </EditorErrorBoundary>

            <Box
                maxH="calc(100vh - 3rem)"
                flex="0 0 15rem"
                bg="#0c0e13"
                color="white"
                overflowY="auto"
                overflowX="visible"
                borderLeft="1px solid #cad5de"
            >
              <InspectorProvider>
                <Inspector />
              </InspectorProvider>
            </Box>
          </Flex>
        </DndProvider>
      </>
  )
})


export default UIBuilder
