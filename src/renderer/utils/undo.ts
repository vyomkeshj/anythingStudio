import { Action } from '@rematch/core'

export default function filterActions(action: Action) {
  if (
    [
      'builderComponents/reset',
      'builderComponents/loadDemo',
      'builderComponents/resetProps',
      'builderComponents/updateProps',
      'builderComponents/addComponent',
      'builderComponents/deleteComponent',
      'builderComponents/moveComponent',
      'builderComponents/addMetaComponent',
      'builderComponents/moveSelectedComponentChildren',
      'builderComponents/duplicate',
    ].includes(action.type)
  ) {
    return true
  }

  return false
}
