import React, {memo} from 'react';

import { DataProvider } from './components/DataContext';
import FusionChartsComponent from './components/FusionChartsComponent';
import {OutputProps} from "../props";

const ChartComponent = memo(({ label, id, outputId, schemaId, ui_message_registry }: OutputProps) => {
    return (
        <DataProvider>
            <FusionChartsComponent type="line" width="600" height="400" ui_message_registry={ui_message_registry} />
        </DataProvider>
    );
});

export default ChartComponent;
