import { Flex } from "@chakra-ui/react";
import React, { memo, useEffect, useState } from "react";
import Divider from "./components/Divider";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Messages from "./components/Messages";
import { OutputProps } from "../props";
import log from "electron-log";

interface ChatInitializationMsg {
  database_schema: string;
  use_model: string;
}

const ChatComponent = memo(({ label, id, outputId, schemaId, useOutputData }: OutputProps) => {
  const [messages, setMessages] = useState([
    { from: "computer", text: "Hi, My Name is ChatQ, Please connect the database and press run to begin!" },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const { last, stale } = useOutputData<string>(outputId);

  const [chatInitMsg, setChatInit] = useState({
    database_schema: "",
    use_model: "",
  });

  useEffect(() => {
    if (last != null) {
      setMessages([{ from: "computer", text: "Connected to database, how can I help you?" }]);
      setChatInit(JSON.parse(last));
    }
  }, [last, stale]);


  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/chat");
    ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((old) => [...old, { from: "computer", text: data.message }]);
    };
    ws.onclose = () => {
      console.log("Disconnected from WebSocket server");
    };
    setSocket(ws);
    return () => {
      ws.close();
    };
  }, []);

  const handleSendMessage = () => {
    if (!inputMessage.trim().length || !socket) {
      return;
    }
    const data = inputMessage;
    console.log(data)
    setMessages((old) => [...old, { from: "me", text: data }]);
    setInputMessage("");

    socket.send(JSON.stringify({ message: data, database_schema:chatInitMsg.database_schema , use_model:chatInitMsg.use_model }));
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
