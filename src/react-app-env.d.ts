/// <reference types="react-scripts" />;
declare module 'prettier/standalone'
declare module 'coloreact'
declare module 'browser-nativefs'

type ComponentType =
  | 'Machines'
  | 'ChatComponent'
  | 'AspectRatio'
  | 'Box'
  | 'Button'
  | 'Center'
  | 'Container'
  | 'Divider'
  | 'Editable'
  | 'Flex'
  | 'Grid'
  | 'Heading'
  | 'Highlight'
  | 'Icon'
  | 'Image'
  | 'Switch'
  | 'Tab'
  | 'Tabs'
  | 'TabList'
  | 'TabPanel'
  | 'TabPanels'

type MetaComponentType =
  | 'MachinesMeta'
  | 'FormControlMeta'
  | 'AccordionMeta'
  | 'ListMeta'
  | 'AlertMeta'
  | 'InputGroupMeta'
  | 'BreadcrumbMeta'
  | 'TabsMeta'
  | 'StatMeta'

export interface IComponent {
  children: string[]
  type: ComponentType
  parent: string
  id: string
  props: any
  rootParentType?: ComponentType
  componentName?: string
}

interface IComponents {
  [name: string]: IComponent
}

interface IPreviewProps {
  component: IComponent
}

interface ComponentItemProps {
  id: string
  label: string
  type: ComponentType
  isMoved?: boolean
  isChild?: boolean
  isMeta?: boolean
  soon?: boolean
  rootParentType?: ComponentType
  children?: React.ReactNode
}
