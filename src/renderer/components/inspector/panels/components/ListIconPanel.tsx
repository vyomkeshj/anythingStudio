import React, { memo } from 'react'
import IconControl from '../../controls/IconControl'
import ColorsControl from '../../controls/ColorsControl'

const ListIconPanel = () => {
  return (
    <>
      <IconControl label="Icon" name="icon" />
      <ColorsControl name="color" label="Color" />
    </>
  )
}

export default memo(ListIconPanel)
