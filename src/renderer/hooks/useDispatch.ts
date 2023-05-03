import { useDispatch as useReduxDispatch } from 'react-redux'
import { RematchDispatch } from '@rematch/core'
import {RootState} from "../redux/store";

const useDispatch = () => {
  return useReduxDispatch() as RematchDispatch<RootState>
}

export default useDispatch
