import React, { memo } from 'react'
import { Select } from '@chakra-ui/react'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import SwitchControl from "../../controls/SwitchControl";
import FormControl from "../../controls/FormControl";
import ColorsControl from "../../controls/ColorsControl";

const SwitchPanel = () => {
  const { setValueFromEvent } = useForm()
  const size = usePropsSelector('size')

  return (
    <>
      <SwitchControl label="Checked" name="isChecked" />

      <FormControl label="Size" htmlFor="size">
        <Select
          name="size"
          id="size"
          size="sm"
          value={size || ''}
          onChange={setValueFromEvent}
        >
          <option>sm</option>
          <option>md</option>
          <option>lg</option>
        </Select>
      </FormControl>

      <ColorsControl label="Color" name="colorScheme" />
    </>
  )
}

export default memo(SwitchPanel)
