import { useSelector } from 'react-redux'
import { useEffect } from 'react'
import { useInspectorUpdate } from "../contexts/inspector-context";
import { RootState } from "../redux/store";
import { getDefaultFormProps } from "../utils/defaultProps";

const usePropsSelector = (propsName: string) => {
  let outputNodes = useSelector((state: RootState) => state.nodes.outputNodes);
  const { addActiveProps } = useInspectorUpdate()

  useEffect(() => {
    // Register form props name for custom props panel
    console.log(propsName)
    addActiveProps(propsName)
  }, [addActiveProps, propsName])

  const value = useSelector((state: RootState) => {
    const component =
      state.builderComponents.components[state.builderComponents.selectedId]
    const propsValue = component.props[propsName]

    if (propsValue !== undefined) {
      return propsValue
    }

    if (getDefaultFormProps(component.type, outputNodes)[propsName] !== undefined) {
      return getDefaultFormProps(component.type, outputNodes)[propsName]
    }

    return ''
  })

  return value
}

export default usePropsSelector
