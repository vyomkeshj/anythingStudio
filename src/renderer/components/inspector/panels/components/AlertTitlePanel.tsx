import React, { memo } from 'react'
import usePropsSelector from "../../../../hooks/usePropsSelector";
import ChildrenControl from "../../controls/ChildrenControl";
import SizeControl from "../../controls/SizeControl";

const AlertTitlePanel = () => {
  const fontSize = usePropsSelector('fontSize')

  return (
    <>
      <ChildrenControl />
      <SizeControl name="fontSize" label="fontSize" value={fontSize} />
    </>
  )
}

export default memo(AlertTitlePanel)
