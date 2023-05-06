import map from 'lodash/map'
import { RootState } from '../../redux/store'
import { IComponent } from "../../../react-app-env";

export const getComponents = (state: RootState) =>
  state.builderComponents.components

export const getComponentBy = (nameOrId: string | IComponent['id']) => (
  state: RootState,
) => state.builderComponents.components[nameOrId]

export const getSelectedComponent = (state: RootState) =>
  state.builderComponents.components[state.builderComponents.selectedId]

export const getPropsForSelectedComponent = (
  state: RootState,
  propsName: string,
) =>
  state.builderComponents.components[state.builderComponents.selectedId]
    .props[propsName]

export const getSelectedComponentId = (state: RootState) =>
  state.builderComponents.selectedId

export const getIsSelectedComponent = (componentId: IComponent['id']) => (
  state: RootState,
) => state.builderComponents.selectedId === componentId

export const getSelectedComponentChildren = (state: RootState) => {
  return getSelectedComponent(state).children.map((child: string) =>
    getComponentBy(child)(state),
  )
}

export const getSelectedComponentParent = (state: RootState) =>
  state.builderComponents.components[getSelectedComponent(state).parent]

export const getHoveredId = (state: RootState) =>
  state.builderComponents.hoveredId

export const getIsHovered = (id: IComponent['id']) => (state: RootState) =>
  getHoveredId(state) === id

export const getComponentNames = (state: RootState) => {
  const names = map(
    state.builderComponents.components,
    comp => comp.componentName,
  ).filter(comp => !!comp)

  return Array.from(new Set(names))
}
