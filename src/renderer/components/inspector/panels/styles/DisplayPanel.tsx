import React, { memo } from 'react'
import { FormControl, Select } from "@chakra-ui/react";
import FlexPanel from './FlexPanel'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";

const DisplayPanel = () => {
  const { setValueFromEvent } = useForm()
  const display = usePropsSelector('display')

  return (
    <>
      <FormControl label="Display"
                   bg="#2e3748">
        <Select
          size="sm"
          value={display || ''}
          onChange={setValueFromEvent}
          name="display"
        >
          <option>block</option>
          <option>flex</option>
          <option>inline</option>
          <option>grid</option>
          <option>inline-block</option>
        </Select>
      </FormControl>

      {display === 'flex' && <FlexPanel />}
    </>
  )
}

export default memo(DisplayPanel)
