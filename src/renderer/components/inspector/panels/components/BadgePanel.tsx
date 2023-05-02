import React, { memo } from 'react'
import { Select } from '@chakra-ui/react'
import usePropsSelector from "../../../../hooks/usePropsSelector";
import { useForm } from "../../../../hooks/useForm";
import FormControl from "../../controls/FormControl";
import ColorsControl from "../../controls/ColorsControl";


const BadgePanel = () => {
  const { setValueFromEvent } = useForm()
  const variant = usePropsSelector('variant')

  return (
    <>
      <ChildrenControl />

      <FormControl htmlFor="variant" label="Variant">
        <Select
          id="variant"
          onChange={setValueFromEvent}
          name="variant"
          size="sm"
          value={variant || ''}
        >
          <option>solid</option>
          <option>outline</option>
          <option>subtle</option>
        </Select>
      </FormControl>

      <ColorsControl label="Color Scheme" name="colorScheme" />
    </>
  )
}

export default memo(BadgePanel)
