import React, { memo } from 'react'
import { Select } from '@chakra-ui/react'
import SizeControl from '../../controls/SizeControl'
import TextControl from '../../controls/TextControl'
import SwitchControl from '../../controls/SwitchControl'
import FormControl from '../../controls/FormControl'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";

const InputPanel = () => {
  const { setValueFromEvent } = useForm()

  const size = usePropsSelector('size')
  const variant = usePropsSelector('variant')

  return (
    <>
      <SizeControl label="Size" options={['sm', 'md', 'lg']} value={size} />
      <TextControl label="Value" name="value" />
      <TextControl label="Placeholder" name="placeholder" />

      <FormControl htmlFor="variant" label="Variant">
        <Select
          id="variant"
          onChange={setValueFromEvent}
          name="variant"
          size="sm"
          value={variant || ''}
        >
          <option>outline</option>
          <option>unstyled</option>
          <option>flushed</option>
          <option>filled</option>
        </Select>
      </FormControl>

      <SwitchControl label="Invalid" name="isInvalid" />
      <SwitchControl label="Read Only" name="isReadOnly" />
      <SwitchControl label="Width" name="width" />
    </>
  )
}

export default memo(InputPanel)
