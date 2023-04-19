// hooks/useWebSocket.ts
import { useContext, useEffect } from "react";
import log from 'electron-log';
import { ToUIOutputMessage } from "../../common/ui_event_messages";
import { OutputChannel } from "../../common/common-types";
import { WebSocketContext } from "../contexts/WebsocketContext";

type WebSocketMessageHandler<T> = (message: ToUIOutputMessage<T>) => void;
const useWebSocketContext = () => useContext(WebSocketContext);

export const useWebSocket = <T>(
  handlers: Record<string, WebSocketMessageHandler<T>>,
  messageRegistry: OutputChannel[],
  onError?: (event: Event) => void,
  onClose?: (event: CloseEvent) => void
) => {
  const { socket } = useWebSocketContext();

  useEffect(() => {
    if (!socket) {
      log.info('fak from WebSocket: ')
      return;
    }

    const messageListener = (event: MessageEvent) => {
      log.info('Received message from WebSocket: ', event.data)
      try {
        const message: ToUIOutputMessage<T> = JSON.parse(event.data);
        const handler = handlers[message.message_tag];
        // if the message.channel_id matches the channel_id of the message with the same tag in the registry, then we know that the message is for us
        if (handler && messageRegistry.find((reg) => reg.channel_id === message.channel_id)) {
          handler(message);
        } else {
          log.warn(`No handler found for message tag: ${message.message_tag}`);
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
};