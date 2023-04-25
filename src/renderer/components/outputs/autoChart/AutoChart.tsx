import React, { memo, useState } from "react";
import { Chart } from "./components/ChartComponent";
import { OutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import log from "electron-log";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import {Skeleton, Stack} from "@chakra-ui/react";

interface ChartData {
  kind: string;
  data: string;
}

const AutoChart = memo(({ ui_message_registry }: OutputProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [chartType, setChartType] = useState("");
  const [chartData, setChartData] = useState([]);

  const handle_new_input = (message: ToUIOutputMessage<ChartData>) => {
    log.info("AutoChart: submit_text: message: ", message.data);
    try {
      setChartData(JSON.parse(message.data.data));
      setChartType(message.data.kind);
      setIsLoading(false);
    } catch (error) {
      console.error("Failed to parse chart data:", error);
    }
  };


  const handlers = {
    'chart_data': handle_new_input,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  return (
    <div className="flex flex-col px-4 items-center justify-center min-h-screen bg-gradient-to-r from-slate-300 to-indigo-50 overflow-x-hidden">
      <div className="flex flex-col items-center w-full max-w-xl mb-6 gap-6 border-gray-300 bg-indigo-50 dark:text-white dark:bg-black dark:border dark:border-white/20 rounded-2xl p-2">

      </div>
      {(chartData && chartType) ? (
        <div className="w-full max-w-2xl mb-6">
          {isLoading ? (
            <div className="flex items-center justify-center h-40">
              Loading...
            </div>
          ) : (
            <div className="flex items-center justify-center h-96">
              <Chart data={chartData} chartType={chartType} />
            </div>
          )}
        </div>
      ) : (
          <div className="w-full max-w-2xl mb-6" style={{ marginTop: "10px" }}>
            <div className="flex items-center justify-center h-40 mt-2">
              <Stack>
                <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
                <Skeleton startColor="#5a5e62" endColor="#ffffff" height='20px' />
              </Stack>
            </div>
          </div>
      )}
    </div>
  );
});

export default AutoChart;
