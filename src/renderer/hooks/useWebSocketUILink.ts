// hooks/useWebSocket.ts
import { useEffect, useRef, useState } from "react";
import log from 'electron-log';
import { ToUIOutputMessage } from "../../common/ui_event_messages";
// hooks/useWebSocket.ts

type WebSocketMessageHandler<T> = (message: ToUIOutputMessage<T>) => void;

export const useWebSocket = <T>(
  url: string,
  handlers: Record<string, WebSocketMessageHandler<T>>,
  onError?: (event: Event) => void,
  onClose?: (event: CloseEvent) => void,
  reconnectInterval: number = 5000
) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const connect = () => {
    socketRef.current = new WebSocket(url);

    socketRef.current.addEventListener('open', () => {
      log.info('WebSocket connection opened');
      setIsConnected(true);
    });

    socketRef.current.addEventListener('close', (event) => {
      setIsConnected(false);
      if (onClose) {
        onClose(event);
      }
      setTimeout(() => {
        log.info('Attempting to reconnect...');
        connect();
      }, reconnectInterval);
    });

    if (onError) {
      socketRef.current.addEventListener('error', onError);
    }
  };

  useEffect(() => {
    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
        log.info('WebSocket connection closed');
      }
    };
  }, [url]);

  useEffect(() => {
    if (!isConnected || !socketRef.current) {
      return;
    }

    const messageListener = (event: MessageEvent) => {
      try {
        const message: ToUIOutputMessage<T> = JSON.parse(event.data);
        const handler = handlers[message.message_tag];

        if (handler) {
          handler(message);
        } else {
          log.warn(`No handler found for message tag: ${message.message_tag}`);
        }
      } catch (error) {
        log.error('Error while parsing WebSocket message: ', error);
      }
    };

    socketRef.current.removeEventListener('message', messageListener);
    socketRef.current.addEventListener('message', messageListener);

    return () => {
      if (socketRef.current) {
        socketRef.current.removeEventListener('message', messageListener);
      }
    };
  }, [isConnected, handlers]);
};