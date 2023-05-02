import React from 'react'
import { Select } from '@chakra-ui/react'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import ChildrenControl from "../../controls/ChildrenControl";
import SizeControl from "../../controls/SizeControl";
import FormControl from "../../controls/FormControl";
import ColorsControl from "../../controls/ColorsControl";
import SwitchControl from "../../controls/SwitchControl";

const TagPanel = () => {
  const { setValueFromEvent } = useForm()

  const size = usePropsSelector('size')
  const variant = usePropsSelector('variant')
  const rounded = usePropsSelector('rounded')

  return (
    <>
      <ChildrenControl />
      <SizeControl
        options={['sm', 'md', 'lg']}
        name="size"
        label="Size"
        value={size}
      />
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

      <SizeControl name="rounded" label="Border radius" value={rounded} />

      <SwitchControl label="Inline" name="isInline" />
    </>
  )
}

export default TagPanel
