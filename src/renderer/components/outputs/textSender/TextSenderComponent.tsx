import React, { memo, useState } from "react";
import axios from "axios";
import log from "electron-log";
import { UINodeOutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import {Button} from "@chakra-ui/react";
import {ArrowForwardIcon} from "@chakra-ui/icons";


export interface SubmitText {
  submitted_text: string
}

interface SubmittedResponse {
  successful: boolean
}

const TextSenderComponent = memo(({ ui_message_registry }: UINodeOutputProps) => {
  const [inputValue, setInputValue] = useState("");

  const handle_submit_response = (message: ToUIOutputMessage<SubmitText>) => {
    log.info("ChartComponent: handle_new_datapoint: message: ", message.data.submitted_text);
    //todo: if error, pop it up
  };


  const handlers = {
    'submit_response': handle_submit_response,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    const response: SubmitText = { submitted_text: inputValue };
    // send event to backend
    sendMessage('submit_text', response)
  };

  return (
    <div className="flex flex-col px-4 items-center justify-center min-h-screen bg-gradient-to-r from-slate-300 to-indigo-50 overflow-x-hidden">
      <div className="flex flex-col items-center w-full max-w-xl mb-6 gap-6 border-gray-300 bg-indigo-50 dark:text-white dark:bg-black dark:border dark:border-white/20 rounded-2xl p-2">
        <form onSubmit={handleSubmit} className="w-full max-w-xl mb-6">
          <div className="flex flex-row items-center justify-center" style={{ display: "flex", flexDirection: "column"}}>
            <textarea
              id="input"
              rows={3}
              placeholder=""
              className="appearance-none font-inter mt-8 border border-gray-300 dark:border-gray-600 shadow-sm flex flex-col items-center justify-center rounded-lg w-full max-w-md py-2 px-3 bg-custom-gray-bg dark:bg-custom-dark-gray text-gray-700 dark:text-white leading-tight focus:outline-none focus:shadow-outline text-center"
              value={inputValue}
              autoFocus
              onChange={(e) => setInputValue(e.target.value)}
            />
            <Button type="submit" rightIcon={<ArrowForwardIcon />} colorScheme='red' color="#c53030" variant='outline' marginTop="10px">
              Send
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
});

export default TextSenderComponent;
