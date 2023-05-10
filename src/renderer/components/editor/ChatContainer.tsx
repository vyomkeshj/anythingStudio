import React, { FunctionComponent, ComponentClass } from 'react'
import { Box } from '@chakra-ui/react'
import { useInteractive } from "../../hooks/useInteractive";
import { IComponent } from "../../../react-app-env";
import {useSelector} from "react-redux";
import {RootState} from "../../redux/store";

const PreviewContainer: React.FC<{
  component: IComponent
  type: string | FunctionComponent<any> | ComponentClass<any, any>
  componentType: string
  enableVisualHelper?: boolean
  isBoxWrapped?: boolean
}> = ({
  component,
  type,
  componentType,
  enableVisualHelper,
  isBoxWrapped,
  ...forwardedProps
}) => {
  let outputNodes = useSelector((state: RootState) => state.nodes.outputNodes);
  const schemaId = componentType === 'chat' ? "machines:chat:chat_node" : 'auto_chart' ? "machines:chart:autochart" : 'tic_tac_toe' ? "machines:games:tic_tac_toe" : "machines:chart:chart_node"
  console.log(outputNodes)
  // @ts-ignore
  const passedProps = outputNodes.filter((node) => node.payload.schemaId === schemaId)[0].payload
  const componentCopy = JSON.parse(JSON.stringify(component))
  componentCopy.props = {...componentCopy.props, ...passedProps}
  const { props, ref } = useInteractive(componentCopy, enableVisualHelper)
  console.log(componentCopy.props, type)

  const children = React.createElement(type, {
    ...props,
    ...forwardedProps,
    ref,
  })

  if (isBoxWrapped) {
    let boxProps: any = {}

    return (
      <Box {...boxProps} ref={ref}>
        {children}
      </Box>
    )
  }

  return children
}

export default PreviewContainer
