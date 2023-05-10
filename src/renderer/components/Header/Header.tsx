import {Box, HStack, SimpleGrid, Tab, TabList, TabPanel, TabPanels, Tabs} from '@chakra-ui/react';
import { memo } from 'react';
// import { DependencyManagerButton } from '../DependencyManagerButton';
import { SettingsButton } from '../SettingsModal';
// import { SystemStats } from '../SystemStats';
import { useDispatch } from 'react-redux';
import { switchToDesigner, switchToEngine } from '../../redux/slices/settingsSlice';
import { AppInfo } from './AppInfo';
import { ExecutionButtons } from './ExecutionButtons';
import { AppDispatch, RootState } from "../../redux/store";

export const Header = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    return (
        <Box
            bg="var(--header-bg)"
            w="100%"
        >
            <SimpleGrid
                columns={5}
                h="56px"
                w="100%"
                spacing={3}
            >
                <AppInfo />
                <HStack></HStack>
                <ExecutionButtons />
                <SettingsButton />

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

