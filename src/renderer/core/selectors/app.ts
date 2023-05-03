import { RootState } from '../../redux/store'

export const getShowLayout = (state: RootState) => state.builder.showLayout

export const getShowCode = (state: RootState) => state.builder.showCode

export const getFocusedComponent = (id: IComponent['id']) => (
  state: RootState,
) => state.builder.inputTextFocused && state.builderComponents.selectedId === id

export const getInputTextFocused = (state: RootState) =>
  state.builder.inputTextFocused
