import { CloseIcon, SearchIcon } from '@chakra-ui/icons';
import { Box, createMultiStyleConfigHelpers, HStack, IconButton, Input, InputGroup, InputLeftElement, InputRightElement, SimpleGrid, Tab, TabList, TabPanel, TabPanels, Tabs } from '@chakra-ui/react';
import { dispatch } from 'd3';
import { ChangeEventHandler, memo } from 'react';
import {useDispatch} from 'react-redux';
import { switchToDesigner, switchToEngine } from '../../redux/slices/settingsSlice';
// import { DependencyManagerButton } from '../DependencyManagerButton';
// import { SettingsButton } from '../SettingsModal';
// import { SystemStats } from '../SystemStats';
import { AppInfo } from './AppInfo';
import { ExecutionButtons } from './ExecutionButtons';
import { AppDispatch, RootState } from "../../redux/store";

	
	export const Header = memo(() => {
		const dispatch = useDispatch<AppDispatch>();

		return (
			<Tabs 
			zIndex={99999}
			variant={'unstyled'} 
			bg="gray.500"
			width={"100%"}
			>
			<TabList>
			<Tab 
			 onClick={() => dispatch(switchToEngine())}
			fontSize={13} 
			_selected={{bg: "var(--selected-tab-color)"}}>
				<HStack>
				<Box minW={"130px"}>
					MachineFlow
				</Box>
				</HStack>
			</Tab>
			<Tab 
			onClick={() => dispatch(switchToDesigner())}
			fontSize={13} 
			_selected={{bg: "var(--selected-tab-color)"}}
			borderRight={"1px solid var(--selected-tab-color)"}
			>
				<HStack>
				<Box minW={"130px"}>
					UI Builder
				</Box>
				</HStack>
				{/* <IconButton
                    aria-label='close tab'
					_hover={{
						bg: "white", 
						color:"var(--gray-500)"
					}}
                    icon={<CloseIcon scale={0.9}/>}
                    size="xs"
                    variant="filled"
                /> */}
			</Tab>
			</TabList>
			</Tabs>
			);
		});
		
		// <Center w="full">
		//     <SystemStats />
		//     <DependencyManagerButton />
		//     <SettingsButton />
		// </Center>
		