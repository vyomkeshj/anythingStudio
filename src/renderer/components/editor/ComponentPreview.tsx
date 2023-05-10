import React, { memo } from "react";
import { useSelector } from "react-redux";

import * as Chakra from "@chakra-ui/react";
import { getComponentBy } from "../../core/selectors/components";
import PreviewContainer from "./PreviewContainer";
import WithChildrenPreviewContainer from "./WithChildrenPreviewContainer";
import AspectRatioPreview from "./previews/AspectRatioBoxPreview";
import IconPreview from "./previews/IconPreview";
import AutoChart from "../outputs/autoChart/AutoChart";
import ChatComponent from "../outputs/chat/ChatComponent";
import ChatContainer from "./ChatContainer";
import TicTacToeComponent from "../outputs/ticTacToe/TicTacToeComponent";
import ChartComponent from "../outputs/chart/ChartComponent";

const ComponentPreview: React.FC<{
  componentName: string
}> = ({ componentName, ...forwardedProps }) => {
  const component = useSelector(getComponentBy(componentName))
  if (!component) {
    console.error(`ComponentPreview unavailable for component ${componentName}`)
  }

  const type = (component && component.type) || null

  switch (type) {
    // Simple components
    case 'Image':
    case 'Heading':
    case 'Switch':
    case 'TabPanel':
    case 'Tab':
      return (
        <PreviewContainer
          component={component}
            // @ts-ignore
          type={Chakra[type]}
          {...forwardedProps}
        />
      )
    case 'AutoChart':
      return (
          <ChatContainer
              component={component}
              // @ts-ignore
              type={AutoChart}
              componentType="auto_chart"
              {...forwardedProps}
          />
      )
    case 'ChatComponent':
      return (
          <ChatContainer
              component={component}
              // @ts-ignore
              type={ChatComponent}
              componentType="chat"
              {...forwardedProps}
          />
      )
    case 'TicTacToe':
      return (
          <ChatContainer
              component={component}
              // @ts-ignore
              type={TicTacToeComponent}
              componentType="tic_tac_toe"
              {...forwardedProps}
          />
      )
    case 'LiveChart':
      return (
          <ChatContainer
              component={component}
              // @ts-ignore
              type={ChartComponent}
              componentType="tic_tac_toe"
              {...forwardedProps}
          />
      )
    // Wrapped functional components (forward ref issue)
    case 'Divider':
      return (
        <PreviewContainer
          component={component}
          type={Chakra[type]}
          {...forwardedProps}
          isBoxWrapped
        />
      )
    // Components with children
    case 'Box':
    case 'Flex':
    case 'Tabs':
    case 'TabList':
    case 'TabPanels':
    case 'Grid':
    case 'Center':
    case 'Container':
      return (
        <WithChildrenPreviewContainer
          enableVisualHelper
          component={component}
          type={Chakra[type]}
          {...forwardedProps}
        />
      )
    case 'AspectRatio':
      return <AspectRatioPreview component={component} />
    case 'Icon':
      return <IconPreview component={component} />
    // case 'ChatComponent':
    //   // @ts-ignore
    //   return <WithChildrenPreviewContainer
    //       enableVisualHelper
    //       component={component}
    //       type={ChatComponent}
    //       {...forwardedProps}
    //   />
    // case 'auto_chart':
    //   // @ts-ignore
    //   return <AutoChart {...forwardedProps} />
    default:
      return null
  }
}

export default memo(ComponentPreview)
