import {Box, HStack, SimpleGrid, Tab, TabList, TabPanel, TabPanels, Tabs} from '@chakra-ui/react';
import { memo } from 'react';
// import { DependencyManagerButton } from '../DependencyManagerButton';
// import { SettingsButton } from '../SettingsModal';
// import { SystemStats } from '../SystemStats';
import { useSelector, useDispatch } from 'react-redux';
import { switchToDesigner, switchToEngine } from '../../redux/slices/settingsSlice';
import { AppInfo } from './AppInfo';
import { ExecutionButtons } from './ExecutionButtons';
import { AppDispatch, RootState } from "../../redux/store";

export const Header = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    // @ts-ignore
    const tab = useSelector((state: RootState) => state.settings.tab);
    return (
        <Box
            bg="var(--header-bg)"
            borderRadius="lg"
            borderWidth="0px"
            h="56px"
            w="100%"
        >
            <SimpleGrid
                columns={3}
                h="100%"
                p={2}
                spacing={3}
            >
                <AppInfo />
                <ExecutionButtons />
                {tab}
                {/*<Box*/}
                {/*    alignContent="right"*/}
                {/*    alignItems="right"*/}
                {/*    w="full"*/}
                {/*>*/}
                {/*    <HStack*/}
                {/*        ml="auto"*/}
                {/*        mr={0}*/}
                {/*        width="fit-content"*/}
                {/*    >*/}
                {/*        /!*<ExecutionButtons />*!/*/}
                {/*    </HStack>*/}
                {/*</Box>*/}
                <Tabs align='end'>
                    <TabList>
                        <Tab onClick={() => dispatch(switchToEngine())}>Engine</Tab>
                        <Tab onClick={() => dispatch(switchToDesigner())}>Designer</Tab>
                    </TabList>
                </Tabs>
            </SimpleGrid>
        </Box>
    );
});

// <Center w="full">
//     <SystemStats />
//     <DependencyManagerButton />
//     <SettingsButton />
// </Center>

