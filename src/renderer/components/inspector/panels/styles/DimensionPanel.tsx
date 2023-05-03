import React, { memo } from 'react'
import { SimpleGrid, Select } from '@chakra-ui/react'
import { useForm } from "../../../../hooks/useForm";
import usePropsSelector from "../../../../hooks/usePropsSelector";
import TextControl from "../../controls/TextControl";
import FormControl from "../../controls/FormControl";

const DimensionPanel = () => {
  const { setValueFromEvent } = useForm()
  const overflow = usePropsSelector('overflow')

  return (
    <>
      <SimpleGrid columns={2} spacingX={1}
                  bg="#2e3748">
        <TextControl label="Width" name="width" />
        <TextControl label="Height" name="height" />
      </SimpleGrid>

      <SimpleGrid columns={2} spacingX={1}
                  bg="#2e3748">
        <TextControl label="Min W" name="minWidth" />
        <TextControl label="Min H" name="minHeight" />

        <TextControl label="Max W" name="maxWidth" />
        <TextControl label="Max H" name="maxHeight" />
      </SimpleGrid>

      <FormControl label="Overflow"
                   bg="#2e3748">
        <Select
          size="sm"
          value={overflow || ''}
          onChange={setValueFromEvent}
          name="overflow"
        >
          <option>visible</option>
          <option>hidden</option>
          <option>scroll</option>
        </Select>
      </FormControl>
    </>
  )
}

export default memo(DimensionPanel)
