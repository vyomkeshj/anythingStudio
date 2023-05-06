import React, { memo } from "react";
import ChatComponent from "../outputs/chat/ChatComponent";
import { UINodeOutputProps } from "../outputs/props";
import MachinesPreviewContainer from "./MachinesPreviewContainer";

const MachinesUIComponentPreview: React.FC<{
  componentName: string
  props: UINodeOutputProps,
}> = ({ componentName, props }) => {

  switch (componentName) {
    // UI Components
    case 'ChatComponent':
      return (
        <MachinesPreviewContainer
          type={ChatComponent}
          machines_node_props={props}
        />
      )
    default:
      return null
  }
}

export default memo(MachinesUIComponentPreview)
