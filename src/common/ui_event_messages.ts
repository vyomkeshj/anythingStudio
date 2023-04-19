
export type ChannelId = string & { readonly __channelId: never };


// Message sent from the backend node to the UI node
export interface ToUIOutputMessage<T> {
  readonly channel_id: ChannelId;

  readonly message_tag: string
  readonly data: T
}
