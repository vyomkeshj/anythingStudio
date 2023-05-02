import {Box, HStack, SimpleGrid, Tab, TabList, TabPanel, TabPanels, Tabs} from '@chakra-ui/react';
import { memo } from 'react';
// import { DependencyManagerButton } from '../DependencyManagerButton';
// import { SettingsButton } from '../SettingsModal';
// import { SystemStats } from '../SystemStats';
import { AppInfo } from './AppInfo';
import { ExecutionButtons } from './ExecutionButtons';

export const Header = memo(() => {
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
                <Tabs align='end'>
                    <TabList>
                        <Tab>Machine</Tab>
                        <Tab>Interface</Tab>
                    </TabList>
                    {/*<TabPanels>*/}
                    {/*    <TabPanel>*/}
                    {/*        <p>one!</p>*/}
                    {/*    </TabPanel>*/}
                    {/*    <TabPanel>*/}
                    {/*        <p>two!</p>*/}
                    {/*    </TabPanel>*/}
                    {/*</TabPanels>*/}
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
