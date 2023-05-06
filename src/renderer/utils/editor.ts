// const ALERT_COMPONENTS: (ComponentType | MetaComponentType)[] = [
//   'Alert',
//   'AlertDescription',
//   'AlertIcon',
//   'AlertTitle',
// ]

export const COMPONENTS: (ComponentType | MetaComponentType)[] = [
  'Box',
  'Button',
  'Center',
  'Container',
  'Divider',
  'Flex',
  'Grid',
  'Heading',
  'Highlight',
  'Icon',
  'Image',
  'Switch',
  'Tab',
  'Editable',
  'AspectRatio',
  'Tab',
  'TabList',
  'TabPanel',
  'TabPanels',
  'Tabs',
  // Allow meta components
  'TabsMeta',
  'ChatComponent',
]

// export const AccordionWhitelist: (
//   | ComponentType
//   | MetaComponentType
// )[] = COMPONENTS.filter(name => !ALERT_COMPONENTS.includes(name))

export const rootComponents = COMPONENTS
  // Remove specific components
  .filter(
    name =>
      ![
        'AlertIcon',
        'AlertDescription',
        'AlertTitle',
        'AvatarBadge',
        'AccordionButton',
        'AccordionPanel',
        'AccordionIcon',
        'BreadcrumbItem',
        'BreadcrumbLink',
      ].includes(name),
  )
