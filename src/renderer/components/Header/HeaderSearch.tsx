import { Box, Button, Card, HStack, IconButton, SimpleGrid, Tag, Text } from '@chakra-ui/react';
import { memo } from 'react';
import { BiPlay, BiTargetLock } from 'react-icons/bi';
import { BsZoomIn, BsZoomOut } from 'react-icons/bs';
import { NodeSelector } from '../NodeSelectorPanel/NodeSelectorPanel';
import HeaderUI from "../../components/Header";
import { ExecutionButtons } from './ExecutionButtons';
import { useSelector } from 'react-redux';
import { RootState } from '../../redux/store';

export const HeaderSearch = memo(() => {
    let tab: Number = useSelector((state: RootState) => state.settings.tab);


    return (
        <Box
        bg="var(--header-bg)"
        position={"fixed"}
        top={"0"}
        left={"0"}
        zIndex={9999}
        w="100%"
        style={{
            "WebkitUserSelect": "none",
            "webkitAppRegion":"drag" // DON'T REMOVE! ignore the error it will just work
        }}
        >
        {  tab == 1 ? <HeaderUI /> :
        <SimpleGrid
        columns={3}
        p={2}
        spacing={1}
        >
        <HStack justify={"center"}>
        
        </HStack>
        <HStack>
        <NodeSelector />
        </HStack>
        <HStack justify={"flex-end"}>
        <ExecutionButtons />
        </HStack>
        </SimpleGrid>}
        </Box>
        );
    });
    