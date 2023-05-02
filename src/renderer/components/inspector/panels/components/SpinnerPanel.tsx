import React, { memo } from 'react'
import { Select } from '@chakra-ui/react'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import FormControl from "../../controls/FormControl";
import TextControl from "../../controls/TextControl";
import ColorsControl from "../../controls/ColorsControl";

const SpinnerPanel = () => {
  const { setValueFromEvent } = useForm()

  const size = usePropsSelector('size')

  return (
    <>
      <TextControl label="Label" name="label" />

      <ColorsControl label="Color" name="color" enableHues />

      <ColorsControl label="Empty color" name="emptyColor" enableHues />

      <FormControl label="Size" htmlFor="size">
        <Select
          name="size"
          id="size"
          size="sm"
          value={size || ''}
          onChange={setValueFromEvent}
        >
          <option>xs</option>
          <option>sm</option>
          <option>md</option>
          <option>lg</option>
          <option>xl</option>
        </Select>
      </FormControl>

      <TextControl label="Thickness" name="thickness" />
      <TextControl label="Speed" name="speed" placeholder="0.45s" />
    </>
  )
}

export default memo(SpinnerPanel)
