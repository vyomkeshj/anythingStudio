import React, { memo } from 'react'
import ChildrenControl from '../../controls/ChildrenControl'
import TextControl from '../../controls/TextControl'
import SwitchControl from '../../controls/SwitchControl'

const LinkPanel = () => {
  return (
    <>
      <ChildrenControl />
      <TextControl name="href" label="Href" />
      <SwitchControl label="External" name="isExternal" />
    </>
  )
}

export default memo(LinkPanel)
