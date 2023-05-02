import React, { memo } from 'react'

import { Select } from '@chakra-ui/react'
import usePropsSelector from "../../../../hooks/usePropsSelector";
import { useForm } from "../../../../hooks/useForm";
import ChildrenControl from "../../controls/ChildrenControl";
import SwitchControl from "../../controls/SwitchControl";
import ColorsControl from "../../controls/ColorsControl";
import FormControl from "../../controls/FormControl";

const CheckboxPanel = () => {
  const { setValueFromEvent } = useForm()
  const size = usePropsSelector('size')

  return (
    <>
      <ChildrenControl />
      <SwitchControl label="Checked" name="isChecked" />
      <ColorsControl label="Color Scheme" name="colorScheme" />
      <FormControl label="Size" htmlFor="size">
        <Select
          name="size"
          id="size"
          size="sm"
          value={size || 'md'}
          onChange={setValueFromEvent}
        >
          <option>sm</option>
          <option>md</option>
          <option>lg</option>
        </Select>
      </FormControl>
    </>
  )
}

export default memo(CheckboxPanel)
