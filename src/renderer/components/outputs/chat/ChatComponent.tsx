import { Flex } from "@chakra-ui/react";
import React, { memo, useEffect, useState } from "react";
import Divider from "./components/Divider";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Messages from "./components/Messages";
import { findChannelIdByName, OutputProps } from "../props";
import log from "electron-log";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocket } from "../../../hooks/useWebSocketUILink";

interface ChatInitializationMsg {
  database_schema: string;
  use_model: string;
}

interface MsgFromChatbot {
  msg: string,
}

interface MsgFromUser {
  msg: string,
}

const ChatComponent = memo(({ label, id, outputId, schemaId, useOutputData, ui_message_registry }: OutputProps) => {


  const handle_from_chatbot_msg = (message: ToUIOutputMessage<MsgFromChatbot>) => {
    log.info("Got message from chatbot_x: ", message);
  };

  const handlers = {
    'msg_from_chatbot': handle_from_chatbot_msg,
  };
  log.info("registry: ", ui_message_registry)

  useWebSocket(`ws://localhost:8000/ui_ws`, handlers, ui_message_registry);

  return (
    <Flex w="500dp" h="300dp" justify="center" align="center">
      <Flex w={["100%", "100%", "100%"]} h="90%" flexDir="column">
        <Header />
        <Divider />
        {/*<Messages messages={messages} />*/}
        <Divider />
      </Flex>
    </Flex>
  );
});

export default ChatComponent;
