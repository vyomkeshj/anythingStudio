import React, { FunctionComponent, ComponentClass, useState } from "react";
import { Box } from '@chakra-ui/react'
import { useInteractive } from "../../hooks/useInteractive";
import { OutputProps, UINodeOutputProps } from "../outputs/props";
import { ComponentType, IComponent } from "../../../react-app-env";
import { newUuid } from "@datalayer/jupyter-react";

const MachinesNodePreviewContainer: React.FC<{
  type: string | FunctionComponent<any> | ComponentClass<any, any>
  enableVisualHelper?: boolean
  isBoxWrapped?: boolean
  machines_node_props: UINodeOutputProps
}> = ({
  type,
  enableVisualHelper,
  machines_node_props,
  isBoxWrapped,
  ...forwardedProps
}) => {
  const [component, setComponent] = useState<IComponent>({
    children: [],
    type: "Machines",
    parent: "root",
    id: newUuid(),
    props: machines_node_props,
    rootParentType: "Box",
    componentName: "hello"
  })
  const { ref } = useInteractive(component, enableVisualHelper)

  const children = React.createElement(type, {
    machines_node_props,
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

export default MachinesNodePreviewContainer
