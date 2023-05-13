import { ComponentType } from "../react-app-env";

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
    TicTacToe: {},
    ChatComponent: {},
    AutoChart: {},
    LiveChart: {},
    Tabs: {
        children: {
            Tabs: {},
            Tab: {},
            TabList: {},
            TabPanel: {},
            TabPanels: {},
        },
    },
}

export const componentsList: ComponentType[] = [
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
    'Image',
    'Switch',
    'TicTacToe',
    'LiveChart',
    'AutoChart',
    'ChatComponent',
    'Tab',
    'TabList',
    'TabPanel',
    'TabPanels',
    'Tabs',
]
