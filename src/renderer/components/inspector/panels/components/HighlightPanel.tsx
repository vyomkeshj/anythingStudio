import React, { memo } from 'react'
import TextControl from "../../controls/TextControl";
import ChildrenControl from "../../controls/ChildrenControl";

const HighlightPanel = () => (
  <>
    <ChildrenControl />
    <TextControl label="Query" name="query" />
  </>
)

export default memo(HighlightPanel)
