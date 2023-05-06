export type MenuItem = {
    children?: MenuItems
    soon?: boolean
    rootParentType?: ComponentType
}

type MenuItems = Partial<
    {
        [k in ComponentType]: MenuItem
    }
>

export const menuItems: MenuItems = {
    AspectRatio: {},
    Box: {},
    Center: {},
    Container: {},
    Divider: {},
    Flex: {},
    Grid: {},
    Heading: {},
    Icon: {},
    Image: {},
    Switch: {},
    Tabs: {
        children: {
            Tabs: {},
            Tab: {},
            TabList: {},
            TabPanel: {},
            TabPanels: {},
        },
    },
    Machines: {
        children: {
            Image: {},
        }
    },
}

export const componentsList: ComponentType[] = [
    'Machines',
    'AspectRatio',
    'Box',
    'Center',
    'Container',
    'Divider',
    'Flex',
    'Grid',
    'Heading',
    'Highlight',
    'Icon',
    'IconButton',
    'Image',
    'SimpleGrid',
    'Switch',
    'Tab',
    'TabList',
    'TabPanel',
    'TabPanels',
    'Tabs',
]
