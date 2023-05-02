import React, { ReactNode, useCallback } from 'react'
import { NumberInput, NumberInputProps } from '@chakra-ui/react'
import FormControl from './FormControl'
import { useForm } from '../useForm'
import usePropsSelector from '../usePropsSelector'

type NumberControlPropsType = NumberInputProps & {
  name: string
  label: string | ReactNode
}

const NumberControl: React.FC<NumberControlPropsType> = ({
  name,
  label,
  ...props
}) => {
  const { setValue } = useForm()
  const value = usePropsSelector(name)

  const onChange = useCallback(
    (val: React.ReactText) => {
      setValue(name, val)
    },
    [name, setValue],
  )

  return (
    <FormControl htmlFor={name} label={label}>
      <NumberInput size="sm" value={value} onChange={onChange} {...props} />
    </FormControl>
  )
}

export default NumberControl
