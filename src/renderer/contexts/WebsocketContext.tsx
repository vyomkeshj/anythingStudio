import { createContext, useContext, useState, useEffect } from 'react';
import { OutputChannel } from '../../common/common-types';

import log from 'electron-log';

export interface WebSocketContextValue {
  url: string | null;
  socket: WebSocket | null;
  messageRegistry: OutputChannel[];
}

export const WebSocketContext = createContext<WebSocketContextValue>({
  url: null,
  socket: null,
  messageRegistry: [],
});

interface WebSocketProviderProps {
  url: string;
  children: React.ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ url, children }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    const newSocket = new WebSocket(url);
    setSocket(newSocket);
    log.info('WebSocket connection created');

    return () => {
      if (newSocket) {
        newSocket.close();
        log.info('WebSocket connection closed');
      }
    };
  }, [url]);

  const contextValue = {
    url,
    socket,
    messageRegistry: [],
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};