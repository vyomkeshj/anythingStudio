import React, { memo } from 'react'
import { Select } from "@chakra-ui/react";
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import FormControl from "../../controls/FormControl";

const StatArrowPanel = () => {
  const { setValueFromEvent } = useForm()
  const type = usePropsSelector('type')

  return (
    <>
      <FormControl label="Type" htmlFor="type">
        <Select
          name="type"
          id="type"
          size="sm"
          value={type || ''}
          onChange={setValueFromEvent}
        >
          <option>increase</option>
          <option>decrease</option>
        </Select>
      </FormControl>
    </>
  )
}

export default memo(StatArrowPanel)
