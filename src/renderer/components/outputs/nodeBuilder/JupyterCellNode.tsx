import React, { memo, useState } from "react";
import log from "electron-log";
import { UINodeOutputProps } from "../props";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import { Cell, CellSidebarDefault, Jupyter, Notebook } from "@datalayer/jupyter-react";
import CellToolbar from "./components/cell/CellToolbar";
const SOURCE_EXAMPLE = `
import numpy as np
import matplotlib.pyplot as plt
x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)
y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('A tale of 2 subplots')
ax1.plot(x1, y1, 'o-')
ax1.set_ylabel('Damped oscillation')
ax2.plot(x2, y2, '.-')
ax2.set_xlabel('time (s)')
ax2.set_ylabel('Undamped')
plt.show()
`;

interface SubmitText {
  submitted_text: string;
}

interface SubmittedResponse {
  successful: boolean;
}

const JupyterCellNode = memo(({ ui_message_registry }: UINodeOutputProps) => {
  const [inputValue, setInputValue] = useState("");

  const handle_submit_response = (message: ToUIOutputMessage<SubmitText>) => {
    log.info("ChartComponent: handle_new_datapoint: message: ", message.data.submitted_text);
    setInputValue(message.data.submitted_text);
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
    <div style={{ backgroundColor: "white", height:"1000px", width: "800px" }} onWheel={handleScroll}>
      <Jupyter startDefaultKernel={false} lite={false}>
        <div>
          <CellToolbar />
          <Cell source={inputValue || SOURCE_EXAMPLE} autoStart={false}  />
        </div>
      </Jupyter>
    </div>
  );
});

export default JupyterCellNode;
