import React, { useContext, useEffect, useRef } from 'react';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import PowerCharts from 'fusioncharts/fusioncharts.powercharts';
import { DataContext } from './DataContext';
import log from "electron-log";

// Load FusionCharts modules
Charts(FusionCharts);
PowerCharts(FusionCharts);

interface FusionChartsComponentProps {
    type: string;
    width: string;
    height: string;
}

const FusionChartsComponent: React.FC<FusionChartsComponentProps> = ({ type, width, height }) => {
    const { dataPoints, labels } = useContext(DataContext);
    const chartRef = useRef(null);

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
                        subCaption: 'Using FusionCharts in React',
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

    return <div ref={chartRef} />;
};

export default FusionChartsComponent;
