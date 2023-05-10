import React, { memo, useState } from "react";
import log from "electron-log";
import { UINodeOutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import { Jupyter } from '@datalayer/jupyter-react';
import CellComponents from "./components/cell/CellComponents";


export interface SubmitText {
  submitted_text: string
}

interface SubmittedResponse {
  successful: boolean
}

const NodeBuilderNode = memo(({ ui_message_registry }: UINodeOutputProps) => {
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

  const handleScroll = (event: { deltaY: number; currentTarget: { style: { transform: string } }; }) => {
    const deltaY = event.deltaY;
    const node = event.currentTarget;
    node.style.transform = `translateY(${deltaY}px)`;
  };

  return (
    <div style={{ backgroundColor: "white", height:"800px", width: "800px" }} onWheel={handleScroll}>
      <Jupyter startDefaultKernel={false} lite={false} >
        <CellComponents />
        {/*<Notebook*/}
        {/*  path="/notebooks/ping.ipynb"*/}
        {/*  CellSidebar={CellSidebarDefault}*/}
        {/*/>*/}
      </Jupyter>
    </div>
  );
});

export default NodeBuilderNode;
