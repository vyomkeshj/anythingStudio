
export type ChannelId = string & { readonly __channelId: never };


// Message sent from the backend node to the UI node
export interface ToUIOutputMessage<T> {
  readonly channel_id: ChannelId;

  readonly message_tag: string
  readonly data: T
}

export interface FromUIOutputMessage<T> {
  // Defined inside the websocket handler, must be present before sent
  readonly channel_id: ChannelId | undefined;

  readonly message_tag: string
  readonly data: T
}