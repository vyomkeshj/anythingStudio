import { HStack, IconButton, Tooltip } from '@chakra-ui/react';
import { memo } from 'react';
import { useTranslation } from 'react-i18next';
import { IoPlayCircle, IoStopCircle } from 'react-icons/io5';
import { useContext } from 'use-context-selector';
import { ExecutionContext, ExecutionStatus } from '../../contexts/ExecutionContext';

export const ExecutionButtons = memo(() => {
    const { t } = useTranslation();

    const { run, pause, kill, status } = useContext(ExecutionContext);

    return (
        <HStack style={{
            "webkitAppRegion": "none"// DON'T REMOVE! ignore the error it will just work
        }} justify={"flex-end"}>
            <Tooltip
                closeOnClick
                closeOnMouseDown
                borderRadius={8}
                label={
                    status === ExecutionStatus.PAUSED
                        ? `${t('header.resume', 'Resume')} (F5)`
                        : `${t('header.run', 'Run')} (F5)`
                }
                px={2}
                py={1}
            >
                <IconButton
                    aria-label={t('header.runButton', 'Run button')}
                    colorScheme="blue"
                    disabled={
                        !(status === ExecutionStatus.READY || status === ExecutionStatus.PAUSED)
                    }
                    icon={<IoPlayCircle />}
                    size="sm"
                    variant="outline"
                    onClick={() => {
                        // eslint-disable-next-line @typescript-eslint/no-floating-promises
                        run();
                    }}
                />
            </Tooltip>
            <Tooltip
                closeOnClick
                closeOnMouseDown
                borderRadius={8}
                label={`${t('header.stop', 'Stop')} (F7)`}
                px={2}
                py={1}
            >
                <IconButton
                    aria-label={t('header.stopButton', 'Stop button')}
                    colorScheme="orange"
                    disabled={![ExecutionStatus.RUNNING, ExecutionStatus.PAUSED].includes(status)}
                    icon={<IoStopCircle />}
                    isLoading={ExecutionStatus.KILLING === status}
                    size="sm"
                    variant="outline"
                    onClick={() => {
                        // eslint-disable-next-line @typescript-eslint/no-floating-promises
                        kill();
                    }}
                />
            </Tooltip>
        </HStack>
    );
});
