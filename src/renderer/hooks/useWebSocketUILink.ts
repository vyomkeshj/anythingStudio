// hooks/useWebSocketUILink.ts
import { useContext, useEffect } from "react";
import log from 'electron-log';
import { ToUIOutputMessage, FromUIOutputMessage } from "../../common/ui_event_messages";
import { OutputChannel } from "../../common/common-types";
import { WebSocketContext } from "../contexts/WebsocketContext";

type WebSocketMessageHandler<T> = (message: ToUIOutputMessage<T>) => void;
const useWebSocketContext = () => useContext(WebSocketContext);

export const useWebSocketUILink = <T>(
  handlers: Record<string, WebSocketMessageHandler<T>>,
  messageRegistry: OutputChannel[],
  onError?: (event: Event) => void,
  onClose?: (event: CloseEvent) => void
) => {
  const { socket } = useWebSocketContext();

  const sendMessage = (message_tag: string, data: T) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      log.error('WebSocket is not open. Cannot send message.');
      return;
    }

    const registryEntry = messageRegistry.find((reg) => reg.channel_name === message_tag);

    if (!registryEntry) {
      log.error(`No registry entry found for message tag: ${message_tag}`);
      return;
    }

    const message: FromUIOutputMessage<T> = {
      channel_id: registryEntry.channel_id,
      message_tag: message_tag,
      data: data,
    };

    try {
      const serializedMessage = JSON.stringify(message);
      socket.send(serializedMessage);
      log.info('Sent message to WebSocket: ', serializedMessage);
    } catch (error) {
      log.error('Error while sending WebSocket message: ', error);
    }
  };

  useEffect(() => {
    if (!socket) {
      log.info('fak from WebSocket: ');
      return;
    }

    const messageListener = (event: MessageEvent) => {
      log.info('Received message from WebSocket: ', event.data);
      try {
        const message: ToUIOutputMessage<T> = JSON.parse(event.data);
        const handler = handlers[message.message_tag];
        // if the message.channel_id matches the channel_id of the message with the same tag in the registry, then we know that the message is for us
        if (handler && messageRegistry.find((reg) => reg.channel_id === message.channel_id)) {
          handler(message);
        }
      } catch (error) {
        log.error('Error while parsing WebSocket message: ', error);
      }
    };

    socket.removeEventListener('message', messageListener);
    socket.addEventListener('message', messageListener);

    if (onError) {
      socket.removeEventListener('error', onError);
      socket.addEventListener('error', onError);
    }

    if (onClose) {
      socket.removeEventListener('close', onClose);
      socket.addEventListener('close', onClose);
    }

    return () => {
      if (socket) {
        socket.removeEventListener('message', messageListener);
        if (onError) {
          socket.removeEventListener('error', onError);
        }
        if (onClose) {
          socket.removeEventListener('close', onClose);
        }
      }
    };
  }, [socket, handlers, messageRegistry, onError, onClose]);

  return { sendMessage };
};
