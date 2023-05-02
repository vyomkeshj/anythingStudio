import React, { memo } from 'react'
import { Input } from '@chakra-ui/react'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import FormControl from "../../controls/FormControl";
import SwitchControl from "../../controls/SwitchControl";

const RadioGroupPanel = () => {
  const { setValueFromEvent } = useForm()
  const spacing = usePropsSelector('spacing')

  return (
    <>
      <FormControl label="Spacing">
        <Input
          size="sm"
          value={spacing || ''}
          name="spacing"
          onChange={setValueFromEvent}
        />
      </FormControl>
      <SwitchControl label="Inline" name="isInline" />
    </>
  )
}

export default memo(RadioGroupPanel)
