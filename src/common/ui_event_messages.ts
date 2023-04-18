import { ExpressionJson } from "./types/json";
import { OutputId } from "./common-types";

export type ChannelId = string & { readonly __channelId: never };

export interface UIEvtChannelSchema {
  // unique id of the channel
  readonly channel_id: ChannelId;
  readonly channel_name: string;
  // 'uplink' | 'downlink'
  readonly channel_direction: string;
}

export interface UIMessageProvider {
  // The map from message_tag to the message data type
  readonly message_types: Map<string, any>;
}

// Message sent from the backend node to the UI node
export interface ToUIOutputMessage<T> {
  readonly node_id: string;
  readonly output_id: OutputId;
  readonly channel_id: ChannelId;

  readonly message_tag: string
  readonly data: T
}
