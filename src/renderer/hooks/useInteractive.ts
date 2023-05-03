import { useRef, MouseEvent } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useDrag } from 'react-dnd'
import {
  getIsSelectedComponent,
  getIsHovered,
} from '../core/selectors/components'
import { getShowLayout, getFocusedComponent } from '../core/selectors/app'
import {AppDispatch} from "../redux/store";
import {toggleInputText} from "../redux/slices/uiBuilderSlice";
import {hover, select, unhover} from "../redux/slices/uiBuilderComponentsSlice";

export const useInteractive = (
  component: IComponent,
  enableVisualHelper = false,
  withoutComponentProps = false,
) => {
  const dispatch = useDispatch<AppDispatch>();
  const showLayout = useSelector(getShowLayout)
  const isComponentSelected = useSelector(getIsSelectedComponent(component.id))
  const isHovered = useSelector(getIsHovered(component.id))
  const focusInput = useSelector(getFocusedComponent(component.id))

  const [, drag] = useDrag({
    item: { id: component.id, type: component.type, isMoved: true },
  })

  const ref = useRef<HTMLDivElement>(null)
  let props = {
    ...(withoutComponentProps ? {} : component.props),
    onMouseOver: (event: MouseEvent) => {
      event.stopPropagation()
      dispatch(hover({ componentId: component.id }))
    },
    onMouseOut: () => {
      dispatch(unhover())
    },
    onClick: (event: MouseEvent) => {
      event.preventDefault()
      event.stopPropagation()
      dispatch(select({ selectedId: component.id }))
    },
    onDoubleClick: (event: MouseEvent) => {
      event.preventDefault()
      event.stopPropagation()
      if (!focusInput) {
        dispatch(toggleInputText())
      }
    },
  }

  if (showLayout && enableVisualHelper) {
    props = {
      ...props,
      border: `1px dashed #718096`,
      padding: props.p || props.padding ? props.p || props.padding : 4,
    }
  }

  if (isHovered || isComponentSelected) {
    props = {
      ...props,
      boxShadow: `${focusInput ? '#ffc4c7' : '#4FD1C5'} 0px 0px 0px 2px inset`,
    }
  }

  return { props, ref: drag(ref), drag }
}
