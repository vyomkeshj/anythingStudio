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
                spacing={1}
            >
                <AppInfo />
                <ExecutionButtons />

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
                        <Tab>One</Tab>
                        <Tab>Two</Tab>
                    </TabList>
                    <TabPanels>
                        <TabPanel>
                            <p>one!</p>
                        </TabPanel>
                        <TabPanel>
                            <p>two!</p>
                        </TabPanel>
                    </TabPanels>
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
