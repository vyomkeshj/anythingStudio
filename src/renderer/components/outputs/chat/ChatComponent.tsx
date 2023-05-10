import { Flex } from "@chakra-ui/react";
import React, {memo, useEffect, useState} from "react";
import Divider from "./components/Divider";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Messages from "./components/Messages";
import { ToUIOutputMessage } from "../../../../common/ui_event_messages";
import { useWebSocketUILink } from "../../../hooks/useWebSocketUILink";
import { UINodeOutputProps } from "../props";

interface MsgFromChatbot {
  msg: string;
}

interface MsgFromUser {
  msg: string;
}

const ChatComponent = memo(({ ui_message_registry }: UINodeOutputProps) => {
  const [messages, setMessages] = useState([
    { from: "computer", text: "Press run to begin!" },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  useEffect(() => {
    console.log(ui_message_registry)
  }, [])
  const handle_from_chatbot_msg = (message: ToUIOutputMessage<MsgFromChatbot>) => {
    setMessages((old) => [...old, { from: "computer", text: message.data.msg }]);
  };

  const handlers = {
    'msg_from_chatbot': handle_from_chatbot_msg,
  };

  const { sendMessage } = useWebSocketUILink(handlers, ui_message_registry);

  const handleSendMessage = () => {
    if (!inputMessage.trim().length) {
      return;
    }
    const data = inputMessage;
    setMessages((old) => [...old, { from: "me", text: data }]);
    setInputMessage("");

    const message: MsgFromUser = {
      msg: data,
    };

    sendMessage('msg_from_user', message);
  };

  return (
    <Flex w="600dp" h="600dp" justify="center" align="center">
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
