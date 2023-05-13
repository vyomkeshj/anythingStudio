import React, { memo, useCallback, useEffect, useState } from "react";

import { DataProvider } from './components/DataContext';
import FusionChartsComponent from './components/FusionChartsComponent';
import { UINodeOutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import log from "electron-log";

interface ChangeChartTypeMsg {
  new_type: string,
}

const ChartComponent = memo(({ ui_message_registry }: UINodeOutputProps) => {
  const [currentGraph, setCurrentGraph] = useState('pie2d')

  const handle_chart_change = (message: ToUIOutputMessage<ChangeChartTypeMsg>) => {
    log.info("ChartComponent: handle_new_datapoint: message: ", message.data.new_type);
    setCurrentGraph(message.data.new_type);
  };


  const handlers = {
    'change_type': handle_chart_change,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  return (
        <DataProvider>
            <FusionChartsComponent type={currentGraph} width="600" height="400" ui_message_registry={ui_message_registry} />
        </DataProvider>
    );
});

export default ChartComponent;
