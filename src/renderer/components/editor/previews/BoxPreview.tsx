import React from 'react'
import { Box } from '@chakra-ui/react'
import { useDropComponent } from "../../../hooks/useDropComponent";
import { useInteractive } from "../../../hooks/useInteractive";
import ComponentPreview from "../ComponentPreview";
import { IComponent } from "../../../../react-app-env";

const BoxPreview: React.FC<{ component: IComponent }> = ({ component }) => {
  const { drop, isOver } = useDropComponent(component.id)
  const { props, ref } = useInteractive(component, true)

  if (isOver) {
    props.bg = 'teal.50'
  }

  return (
    <Box pos="relative" ref={drop(ref)} {...props}>
      {component.children.map((key: string) => (
        <ComponentPreview key={key} componentName={key} />
      ))}
    </Box>
  )
}

export default BoxPreview
