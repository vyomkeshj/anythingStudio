import { Flex } from "@chakra-ui/react";
import React, { memo, useEffect, useState } from "react";
import Divider from "./components/Divider";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Messages from "./components/Messages";
import { OutputProps } from "../props";
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

const ChatComponent = memo(({ label, id, outputId, schemaId, useOutputData, ui_message_registry }: OutputProps) => {
  const [messages, setMessages] = useState([
    { from: "computer", text: "Hi, My Name is ChatQ, Please connect the database and press run to begin!" },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  // const [socket, setSocket] = useState<WebSocket | null>(null);
  // const { last, stale } = useOutputData<string>(outputId);
  // // log.info("channels = "+ui_message_registry)
  //
  // const [chatInitMsg, setChatInit] = useState({
  //   database_schema: "",
  //   use_model: "",
  // });
  //
  // useEffect(() => {
  //   if (last != null) {
  //     setMessages([{ from: "computer", text: "Connected to database, how can I help you?" }]);
  //     setChatInit(JSON.parse(last));
  //   }
  // }, [last, stale]);

  const handle_from_chatbot_msg = (message: ToUIOutputMessage<MsgFromChatbot>) => {
    log.info("Got message from chatbot_x: ", message);
    // setMessages([{ from: "computer", text: message.data.msg }]);
  };

  const handlers = {
    'msg_from_chatbot': handle_from_chatbot_msg,
  };

  useWebSocket(`ws://localhost:8000/ui_ws`, handlers);


  const handleSendMessage = () => {
    // if (!inputMessage.trim().length || !socket) {
    //   return;
    // }
    // const data = inputMessage;
    // console.log(data)
    // setMessages((old) => [...old, { from: "me", text: data }]);
    // setInputMessage("");
    //
    // socket.send(JSON.stringify({ message: data, database_schema:chatInitMsg.database_schema , use_model:chatInitMsg.use_model }));
  };

  return (
    <Flex w="500dp" h="300dp" justify="center" align="center">
      <Flex w={["100%", "100%", "100%"]} h="90%" flexDir="column">
        <Header />
        <Divider />
        <Messages messages={messages} />
        <Divider />
        <Footer
          inputMessage={inputMessage}
          setInputMessage={setInputMessage}
          handleSendMessage={handleSendMessage}
        />
      </Flex>
    </Flex>
  );
});

export default ChatComponent;
