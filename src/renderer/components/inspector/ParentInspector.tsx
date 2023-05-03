import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { getSelectedComponentParent } from "../../core/selectors/components";
import ElementListItem from "./elements-list/ElementListItem";
import {AppDispatch} from "../../redux/store";
import {hover, select, unhover} from "../../redux/slices/uiBuilderComponentsSlice";

const ParentInspector = () => {
  const parentComponent = useSelector(getSelectedComponentParent)
  const dispatch = useDispatch<AppDispatch>();

  const onSelect = () => {
    dispatch(select({ selectedId: parentComponent.id }))
  }

  const onHover = () => {
    dispatch(hover({ componentId: parentComponent.id }))
  }

  const onUnhover = () => {
    dispatch(unhover())
  }

  return (
    <ElementListItem
      type={parentComponent.type}
      onMouseOver={onHover}
      onMouseOut={onUnhover}
      onSelect={onSelect}
    />
  )
}

export default ParentInspector
