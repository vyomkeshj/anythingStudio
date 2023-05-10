import Composer from './composer'
import { IComponents } from "../../react-app-env";
import ChatComponent from "../components/outputs/chat/ChatComponent";

type ComposedComponent = {
  components: IComponents
  root: string
  parent: string
}


export const buildMachinesComponent = (parent: string): ComposedComponent => {
  const composer = new Composer()

  const nodeId = composer.addNode({ type: 'Machines', parent })

  // composer.addNode({ type: ChatComponent, parent: nodeId })

  const components = composer.getComponents()

  return {
    components,
    root: nodeId,
    parent,
  }
}


export const buildTabs = (parent: string): ComposedComponent => {
  const composer = new Composer('Tabs')

  const nodeId = composer.addNode({ type: 'Tabs', parent })
  const tabListId = composer.addNode({ type: 'TabList', parent: nodeId })
  const tabPanelsId = composer.addNode({ type: 'TabPanels', parent: nodeId })

  composer.addNode({
    type: 'Tab',
    parent: tabListId,
    props: { children: 'One' },
  })
  composer.addNode({
    type: 'Tab',
    parent: tabListId,
    props: { children: 'Two' },
  })

  composer.addNode({
    type: 'TabPanel',
    parent: tabPanelsId,
    props: { children: 'One !' },
  })
  composer.addNode({
    type: 'TabPanel',
    parent: tabPanelsId,
    props: { children: 'Two !' },
  })

  const components = composer.getComponents()

  return {
    components,
    root: nodeId,
    parent,
  }
}


type BuilderFn = (parent: string) => ComposedComponent

type ComposerBuilders = {
  [k: string]: BuilderFn
}

const builders: ComposerBuilders = {
  MachinesMeta: buildMachinesComponent,
  TabsMeta: buildTabs,
}

export default builders
