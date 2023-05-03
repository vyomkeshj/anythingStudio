import React from 'react'
import { MenuItem, Box } from '@chakra-ui/react'
import { FiUpload } from 'react-icons/fi'
import { loadFromJSON } from "../../utils/import";
import {useDispatch} from "react-redux";
import {AppDispatch} from "../../redux/store";
import {reset} from "../../redux/slices/uiBuilderComponentsSlice";

const ImportMenuItem = () => {
    const dispatch = useDispatch<AppDispatch>();

  return (
    <MenuItem
      onClick={async () => {
        const components = await loadFromJSON()
        dispatch(reset(components))
      }}
    >
      <Box mr={2} as={FiUpload} />
      Import components
    </MenuItem>
  )
}

export default ImportMenuItem
