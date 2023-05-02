import React, { memo } from 'react'
import usePropsSelector from '../usePropsSelector'
import SwitchControl from '~components/inspector/controls/SwitchControl'
import { Input } from '@chakra-ui/react'
import { useForm } from '../useForm'
import FormControl from '~components/inspector/controls/FormControl'

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
