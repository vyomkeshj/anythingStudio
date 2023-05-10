import { useDrop, DropTargetMonitor } from 'react-dnd'
import { useDispatch } from 'react-redux'
import builder from "../composer/builder";
import { rootComponents } from "../utils/editor";
import {AppDispatch} from "../redux/store";
import {addComponent, addMetaComponent, moveComponent} from "../redux/slices/uiBuilderComponentsSlice";
import { ComponentItemProps, ComponentType, MetaComponentType } from "../../react-app-env";

export const useDropComponent = (
  componentId: string,
  accept: (ComponentType | MetaComponentType)[] = rootComponents,
  canDrop: boolean = true,
) => {
  const dispatch = useDispatch<AppDispatch>();

  const [{ isOver }, drop] = useDrop({
    accept,
    collect: monitor => ({
      isOver: monitor.isOver({ shallow: true }) && monitor.canDrop(),
    }),
    drop: (item: ComponentItemProps, monitor: DropTargetMonitor) => {
      if (!monitor.isOver()) {
        return
      }
      console.log(item)
      if (item.isMoved) {
        dispatch(moveComponent({
          parentId: componentId,
          componentId: item.id,
        }))
      } else if (item.isMeta) {
        dispatch(addMetaComponent(builder[item.type](componentId)))
      } else {
        dispatch(addComponent({
          parentName: componentId,
          type: item.type,
          rootParentType: item.rootParentType,
        }))
      }
    },
    canDrop: () => canDrop,
  })

  return { drop, isOver }
}
