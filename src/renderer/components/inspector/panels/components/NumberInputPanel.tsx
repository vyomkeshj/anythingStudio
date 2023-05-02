import React, { memo } from 'react'
import SwitchControl from "../../controls/SwitchControl";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import SizeControl from "../../controls/SizeControl";
import TextControl from "../../controls/TextControl";
import NumberControl from "../../controls/NumberControl";

const NumberInputPanel = () => {
  const size = usePropsSelector('size')

  return (
    <>
      <SizeControl label="Size" options={['sm', 'md', 'lg']} value={size} />
      <TextControl label="Value" name="value" />
      <NumberControl name="step" label="Step" />
      <NumberControl name="precision" label="Precision" />

      <SwitchControl label="Invalid" name="isInvalid" />
      <SwitchControl label="Read Only" name="isReadOnly" />
      <SwitchControl label="Width" name="width" />
    </>
  )
}

export default memo(NumberInputPanel)
