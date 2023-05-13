import React from 'react'
import { Box, AspectRatio } from '@chakra-ui/react'
import ComponentPreview from "../ComponentPreview";
import { useDropComponent } from "../../../hooks/useDropComponent";
import { useInteractive } from "../../../hooks/useInteractive";
import { IComponent } from "../../../../react-app-env";

const AspectRatioPreview: React.FC<{ component: IComponent }> = ({
  component,
}) => {
  const { props, ref } = useInteractive(component, true)
  const { drop, isOver } = useDropComponent(
    component.id,
    undefined,
    component.children.length === 0,
  )
  const children = component.children

  const boxProps: any = {}

  if (isOver) {
    props.bg = 'teal.50'
  }

  return (
    <Box {...boxProps} ref={drop(ref)}>
      <AspectRatio {...props}>
        {!children.length ? (
          /*
           * We need at least one children because of the implementation
           * of AspectRatio
           */
          <Box />
        ) : (
          <Box>
            <ComponentPreview componentName={children[0]} />
          </Box>
        )}
      </AspectRatio>
    </Box>
  )
}

export default AspectRatioPreview
