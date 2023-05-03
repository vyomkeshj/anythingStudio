import useDispatch from './useDispatch'
import { useSelector } from 'react-redux'
import { ActionCreators as UndoActionCreators } from 'redux-undo'
import { useHotkeys } from 'react-hotkeys-hook'
import {deleteComponent,unselect,selectParent,duplicate,loadDemo} from "../redux/slices/uiBuilderComponentsSlice";
import {toggleBuilderMode,toggleCodePanel} from "../redux/slices/uiBuilderSlice";
import {RootState} from "../redux/store";

const keyMap = {
  DELETE_NODE: 'Backspace, del',
  TOGGLE_BUILDER_MODE: 'b',
  TOGGLE_CODE_PANEL: 'c',
  UNDO: 'ctrl+z, command+z',
  REDO: 'ctrl+y, cmd+y',
  UNSELECT: 'esc',
  PARENT: 'p',
  DUPLICATE: 'ctrl+d, command+d',
  KONAMI_CODE:
    'up up down down left right left right b a, up up down down left right left right B A',
}

const hasNoSpecialKeyPressed = (event: KeyboardEvent | undefined) =>
  !event?.metaKey && !event?.shiftKey && !event?.ctrlKey && !event?.altKey

const useShortcuts = () => {
  const dispatch = useDispatch()
  const selected = useSelector((state: RootState) =>
      state.builderComponents.present.components[state.builderComponents.present.selectedId])

  const deleteNode = (event: KeyboardEvent | undefined) => {
    if (event) {
      event.preventDefault()
    }
    dispatch(deleteComponent({ componentId: selected.id }))
  }

  const toggleBuilderModeFn = (event: KeyboardEvent | undefined) => {
    if (event && hasNoSpecialKeyPressed(event)) {
      event.preventDefault()
      dispatch(toggleBuilderMode())
    }
  }

  const toggleCodePanelFn = (event: KeyboardEvent | undefined) => {
    if (event && hasNoSpecialKeyPressed(event)) {
      event.preventDefault()
      dispatch(toggleCodePanel())
    }
  }

  const undo = (event: KeyboardEvent | undefined) => {
    if (event) {
      event.preventDefault()
    }

    dispatch(UndoActionCreators.undo())
  }

  const redo = (event: KeyboardEvent | undefined) => {
    if (event) {
      event.preventDefault()
    }

    dispatch(UndoActionCreators.redo())
  }

  const onUnselect = () => {
    dispatch(unselect())
  }

  const onSelectParent = (event: KeyboardEvent | undefined) => {
    if (event && hasNoSpecialKeyPressed(event)) {
      event.preventDefault()
      dispatch(selectParent())
    }
  }

  const onDuplicate = (event: KeyboardEvent | undefined) => {
    if (event) {
      event.preventDefault()
    }

    dispatch(duplicate())
  }

  const onKonamiCode = () => {
    dispatch(loadDemo({ type: 'secretchakra'}))
  }
  //
  // useHotkeys(keyMap.DELETE_NODE, deleteNode, {}, [selected.id])
  // useHotkeys(keyMap.TOGGLE_BUILDER_MODE, toggleBuilderModeFn)
  // useHotkeys(keyMap.TOGGLE_CODE_PANEL, toggleCodePanelFn)
  // useHotkeys(keyMap.UNDO, undo)
  // useHotkeys(keyMap.REDO, redo)
  // useHotkeys(keyMap.UNSELECT, onUnselect)
  // useHotkeys(keyMap.PARENT, onSelectParent)
  // useHotkeys(keyMap.DUPLICATE, onDuplicate)
  // useHotkeys(keyMap.KONAMI_CODE, onKonamiCode)
}

export default useShortcuts
