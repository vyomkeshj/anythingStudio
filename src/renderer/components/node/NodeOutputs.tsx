/* eslint-disable react/jsx-props-no-spreading */

import { NeverType, Type, evaluate } from '@chainner/navi';
import log from 'electron-log';
import { memo, useCallback, useEffect } from 'react';
import { useContext, useContextSelector } from 'use-context-selector';
import { NodeData, Output, OutputId, OutputKind, SchemaId } from "../../../common/common-types";
import { ExpressionJson, fromJson } from '../../../common/types/json';
import { getMachinesStudioScope } from '../../../common/types/machines-scope';
import { isStartingNode } from "../../../common/util";
import { BackendContext } from '../../contexts/BackendContext';
import { GlobalContext, GlobalVolatileContext } from '../../contexts/GlobalNodeState';
import { HtmlOutput } from '../outputs/HtmlOutput';
import { DefaultImageOutput } from '../outputs/DefaultImageOutput';
import { GenericOutput } from '../outputs/GenericOutput';
import { LargeImageOutput } from '../outputs/LargeImageOutput';
import { MarkdownOutput } from "../outputs/MarkdownOutput";
import { OutputContainer } from '../outputs/OutputContainer';
import { OutputProps, UseOutputData } from '../outputs/props';
import { TaggedOutput } from '../outputs/TaggedOutput';
import ChatComponent from "../outputs/chat/ChatComponent";
import TicTacToeComponent from "../outputs/ticTacToe/TicTacToeComponent";
import ChartComponent from "../outputs/chart/ChartComponent";
import AutoChart from "../outputs/autoChart/AutoChart";
import TextSenderComponent from "../outputs/textSender/TextSenderComponent";
import NodeBuilderNode from "../outputs/nodeBuilder/NodeBuilderNode";

interface FullOutputProps extends Omit<Output, 'id' | 'type'>, OutputProps {
    definitionType: Type;
}

const OutputComponents: Readonly<
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Record<OutputKind, React.MemoExoticComponent<(props: any) => JSX.Element>>
> = {
    jupyter: NodeBuilderNode,
    markdown: MarkdownOutput,
    html: HtmlOutput,
    'text_sender': TextSenderComponent,
    chat: ChatComponent,
    chart: ChartComponent,
    'auto_chart': AutoChart,
    'tic_tac_toe': TicTacToeComponent,
    image: DefaultImageOutput,
    'large-image': LargeImageOutput,
    tagged: TaggedOutput,
    generic: GenericOutput,
};
const OutputIsGeneric: Readonly<Record<OutputKind, boolean>> = {
    'text_sender': false,
    'jupyter': false,
    'tic_tac_toe': false,
    'auto_chart': false,
    markdown: false,
    html: false,
    chat: false,
    chart: false,
    image: true,
    'large-image': false,
    tagged: false,
    generic: true,
};

const pickOutput = (kind: OutputKind, props: FullOutputProps) => {
    const OutputType = OutputComponents[kind];
    return (
        <OutputContainer
            definitionType={props.definitionType}
            generic={OutputIsGeneric[kind]}
            hasHandle={props.hasHandle}
            id={props.id}
            key={`${props.id}-${props.outputId}`}
            label={props.label}
            outputId={props.outputId}
        >
            <OutputType {...props} />
        </OutputContainer>
    );
};

const NO_OUTPUT_DATA: UseOutputData<never> = { current: undefined, last: undefined, stale: false };

interface NodeOutputProps {
    outputs: readonly Output[];
    id: string;
    schemaId: SchemaId;
    animated?: boolean;
    nodeData: NodeData;
}

const evalExpression = (expression: ExpressionJson | null | undefined): Type | undefined => {
    if (expression == null) return undefined;
    try {
        return evaluate(fromJson(expression), getMachinesStudioScope());
    } catch (error) {
        log.error(error);
    }
};

export const NodeOutputs = memo(({ outputs, id, schemaId, animated = false, nodeData}: NodeOutputProps) => {
    const { functionDefinitions, schemata } = useContext(BackendContext);
    const { setManualOutputType } = useContext(GlobalContext);

    const outputDataEntry = useContextSelector(GlobalVolatileContext, (c) =>
        c.outputDataMap.get(id)
    );
    const inputHash = useContextSelector(GlobalVolatileContext, (c) => c.inputHashes.get(id));
    const stale = inputHash !== outputDataEntry?.inputHash;

    const useOutputData = useCallback(
        // eslint-disable-next-line prefer-arrow-functions/prefer-arrow-functions, func-names
        function <T>(outputId: OutputId): UseOutputData<T> {
            if (outputDataEntry) {
                const last = outputDataEntry.data?.[outputId] as T | undefined;
                if (last !== undefined) {
                    return { current: stale ? undefined : last, last, stale };
                }
            }
            return NO_OUTPUT_DATA;
        },
        [outputDataEntry, stale]
    );

    const currentTypes = stale ? undefined : outputDataEntry?.types;

    const schema = schemata.get(schemaId);
    useEffect(() => {
        if (isStartingNode(schema)) {
            for (const output of schema.outputs) {
                // todo: set channels here?
                const type = evalExpression(currentTypes?.[output.id]);
                setManualOutputType(id, output.id, type);
            }
        }
    }, [id, currentTypes, schema, setManualOutputType]);

    const functions = functionDefinitions.get(schemaId)?.outputDefaults;
    return (
        <>
            {outputs.map((output) => {
                const props: FullOutputProps = {
                    ...output,
                    id,
                    ui_message_registry: nodeData.outputChannelData,
                    outputId: output.id,
                    useOutputData,
                    kind: output.kind,
                    schemaId,
                    definitionType: functions?.get(output.id) ?? NeverType.instance,
                    hasHandle: output.hasHandle,
                    animated
                };
                return pickOutput(output.kind, props);
            })}
        </>
    );
});
