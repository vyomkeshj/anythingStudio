import React from 'react'
import { Box, Highlight } from '@chakra-ui/react'
import { useInteractive } from "../../../hooks/useInteractive";

const HighlightPreview: React.FC<IPreviewProps> = ({ component }) => {
  const { props, ref } = useInteractive(component, true, true)

  return (
    <Box {...props} ref={ref}>
      <Highlight {...component.props} styles={component.props} />
    </Box>
  )
}

export default HighlightPreview
