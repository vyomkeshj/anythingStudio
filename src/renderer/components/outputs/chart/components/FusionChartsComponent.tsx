import React, { useContext, useEffect, useRef } from 'react';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import PowerCharts from 'fusioncharts/fusioncharts.powercharts';
import { DataContext } from './DataContext';
import log from "electron-log";
import {ToUIOutputMessage} from "../../../../../common/ui_event_messages";
import {useWebSocketUILink} from "../../../../hooks/useWebSocketUILink";
import {OutputChannel} from "../../../../../common/common-types";
import {Skeleton, Stack} from "@chakra-ui/react";

// Load FusionCharts modules
Charts(FusionCharts);
PowerCharts(FusionCharts);

interface NewDatapoint {
    value: number;
    label: string;
}

interface FusionChartsComponentProps {
    type: string;
    width: string;
    height: string;
    ui_message_registry: OutputChannel[];
}

const FusionChartsComponent: React.FC<FusionChartsComponentProps> = ({ type, width, height, ui_message_registry }) => {
    const { dataPoints, labels, setLabels, setDataPoints } = useContext(DataContext);
    const chartRef = useRef(null);

    const handle_new_datapoint = (message: ToUIOutputMessage<NewDatapoint>) => {
        setLabels(() => [...labels, message.data.label]);
        setDataPoints(() => [...dataPoints, message.data.value]);
    };

    const handlers = {
        'new_datapoint': handle_new_datapoint,
    };

    const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);
    useEffect(()=>{
    }, [labels, dataPoints])
    useEffect(() => {
        if (dataPoints.length > 0 && labels.length > 0) {
            const chartConfig = {
                type,
                width,
                height,
                dataFormat: 'json',
                dataSource: {
                    chart: {
                        caption: 'Data Chart',
                        subCaption: '<More information here>',
                    },
                    data: dataPoints.map((value, index) => ({ value, label: labels[index] })),
                },
            };

            if (chartRef.current) {
                const fusionChartInstance = new FusionCharts(chartConfig);
                fusionChartInstance.render(chartRef.current);
            }
        }
    }, [type, width, height, dataPoints, labels]);

    return (dataPoints.length > 0 ? (<div ref={chartRef} />) :
            (
                <div className="w-full max-w-2xl mb-6" style={{ marginTop: "10px" }}>
                    <div className="flex items-center justify-center h-40 mt-2">
                        <Stack>
                            <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                            <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                            <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                            <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                            <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                        </Stack>
                    </div>
                </div>)
    );
};

export default FusionChartsComponent;
