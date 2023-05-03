import { ChangeEvent, useCallback } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { getSelectedComponentId } from "../core/selectors/components";
import {AppDispatch} from "../redux/store";
import {updateProps} from "../redux/slices/uiBuilderComponentsSlice";

export const useForm = () => {
  const dispatch = useDispatch<AppDispatch>();
  const componentId = useSelector(getSelectedComponentId)

  const setValueFromEvent = ({
    target: { name, value },
  }: ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    setValue(name, value)
  }

  const setValue = useCallback(
    (name: string, value: any) => {
      dispatch(updateProps({
        id: componentId,
        name,
        value,
      }))
    },
    [componentId],
  )

  return { setValue, setValueFromEvent }
}
