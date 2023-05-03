import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { getSelectedComponentChildren } from "../../core/selectors/components";
import ElementsList from "./elements-list/ElementsList";
import {AppDispatch} from "../../redux/store";
import {hover, moveSelectedComponentChildren, select, unhover} from "../../redux/slices/uiBuilderComponentsSlice";

const ChildrenInspector = () => {
  const childrenComponent = useSelector(getSelectedComponentChildren)
  const dispatch = useDispatch<AppDispatch>();

  const moveChildren = (fromIndex: number, toIndex: number) => {
    dispatch(moveSelectedComponentChildren({
      fromIndex,
      toIndex,
    }))
  }

  const onSelectChild = (id: IComponent['id']) => {
    dispatch(select({ selectedId: id }))
  }

  const onHoverChild = (id: IComponent['id']) => {
    dispatch(hover({ componentId: id }))
  }

  const onUnhoverChild = () => {
    dispatch(unhover())
  }

  return (
    <ElementsList
      elements={childrenComponent}
      moveItem={moveChildren}
      onSelect={onSelectChild}
      onHover={onHoverChild}
      onUnhover={onUnhoverChild}
    />
  )
}

export default ChildrenInspector
