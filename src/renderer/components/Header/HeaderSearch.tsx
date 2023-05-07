import { Box, Button, Card, HStack, IconButton, SimpleGrid, Tag, Text } from '@chakra-ui/react';
import { memo } from 'react';
import { BiPlay, BiTargetLock } from 'react-icons/bi';
import { BsZoomIn, BsZoomOut } from 'react-icons/bs';
import { NodeSelector } from '../NodeSelectorPanel/NodeSelectorPanel';
import { ExecutionButtons } from './ExecutionButtons';

export const HeaderSearch = memo(() => {
    return (
        <Box
        bg="var(--header-bg)"
        w="100%"
        style={{
            "WebkitUserSelect": "none",
            "webkitAppRegion":"drag" // DON'T REMOVE! ignore the error it will just work
        }}
        >
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
        </SimpleGrid>
        </Box>
        );
    });
    