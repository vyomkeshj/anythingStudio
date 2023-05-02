import React from 'react'
import { InputRightElement } from '@chakra-ui/react'
import { useDropComponent } from "../../../hooks/useDropComponent";
import { useInteractive } from "../../../hooks/useInteractive";
import ComponentPreview from "../ComponentPreview";

export const InputRightElementPreview: React.FC<{ component: IComponent }> = ({
  component,
}) => {
  const { drop, isOver } = useDropComponent(component.id)
  const { props, ref } = useInteractive(component, true)

  if (isOver) {
    props.bg = 'teal.50'
  }

  return (
    <InputRightElement top="10px" right="10px" {...props} ref={drop(ref)}>
      {component.children.map((key: string) => (
        <ComponentPreview key={key} componentName={key} />
      ))}
    </InputRightElement>
  )
}
