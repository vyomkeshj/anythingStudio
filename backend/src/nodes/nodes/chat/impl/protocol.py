from typing import TypedDict


class MsgFromUser(TypedDict):
    msg: str


class MsgFromChatbot(TypedDict):
    msg: str


class MsgHistoryItem(TypedDict):
    role: str
    content: str
