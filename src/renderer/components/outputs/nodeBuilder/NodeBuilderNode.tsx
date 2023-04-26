import React, { memo, useState } from "react";
import log from "electron-log";
import { OutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import {Button} from "@chakra-ui/react";
import {ArrowForwardIcon} from "@chakra-ui/icons";
import { Cell, CellSidebarDefault, IpyWidgetsComponent, Jupyter, Notebook } from "@datalayer/jupyter-react";
import CellComponents from "./components/cell/CellComponents";
import OutputsComponents from "./components/outputs/OutputsComponents";
import IPyWidgetsSimple from "./components/ipywidgets/IPyWidgetsSimple";


export interface SubmitText {
  submitted_text: string
}

interface SubmittedResponse {
  successful: boolean
}

const NodeBuilderNode = memo(({ ui_message_registry }: OutputProps) => {
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
    <>
      <Jupyter startDefaultKernel={true}>
        <IpyWidgetsComponent Widget={IPyWidgetsSimple}/>
        <OutputsComponents/>
        <CellComponents/>
        <Notebook
          // path={"/ping.ipynb"}
          CellSidebar={CellSidebarDefault}
        />
        {/*
        <FileBrowserTree/>
*/}
      </Jupyter>
      <div className="App">
        <header className="App-header">
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    </>
  );
});

export default NodeBuilderNode;
