import React, { memo, useState } from "react";
import { Chart } from "./components/ChartComponent";
import axios from "axios";
import { OutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import log from "electron-log";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import { SubmitText } from "../text_sender/TextSenderComponent";

const AutoChart = memo(({ ui_message_registry }: OutputProps) => {
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chartType, setChartType] = useState("");
  const [chartData, setChartData] = useState([]);

  const generateChartData = async (prompt: string) => {
    try {
      const response = await axios.post("/api/parse-graph", { prompt });
      console.log(response.data);
      return response.data;
    } catch (error) {
      console.error("Failed to generate chart data:", error);
      throw error;
    }
  };

  const getChartType = async (inputData: string) => {
    try {
      const response = await axios.post("/api/get-type", { inputData });
      return response;
    } catch (error) {
      console.error("Failed to generate chart type:", error);
      throw error;
    }
  };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    setIsLoading(true);
    console.log(inputValue);
    const chartType = await getChartType(inputValue);

    try {
      const libraryPrompt = `Generate a valid JSON in which each element is an object. Strictly using this FORMAT and naming:
[{ "name": "a", "value": 12 }] for the following description for Recharts. \n\n${inputValue}\n`;

      const chartDataGenerate = await generateChartData(libraryPrompt);

      try {
        setChartData(JSON.parse(chartDataGenerate));
        setChartType(chartType.data);
      } catch (error) {
        console.error("Failed to parse chart data:", error);
      }
    } catch (error) {
      console.error("Failed to generate graph data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handle_new_input = (message: ToUIOutputMessage<SubmitText>) => {
    log.info("AutoChart: submit_text: message: ", message.data.submitted_text);
    setInputValue(message.data.submitted_text);
  };


  const handlers = {
    'submit_text': handle_new_input,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  return (
    <div className="flex flex-col px-4 items-center justify-center min-h-screen bg-gradient-to-r from-slate-300 to-indigo-50 overflow-x-hidden">
      <div className="flex flex-col items-center w-full max-w-xl mb-6 gap-6 border-gray-300 bg-indigo-50 dark:text-white dark:bg-black dark:border dark:border-white/20 rounded-2xl p-2">
      </div>
      {chartData && chartType && (
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
      )}
    </div>
  );
});

export default AutoChart;
