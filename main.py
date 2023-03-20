from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent

import config
from services import user_event_service, message_event_service

app = FastAPI()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


# Line Bot only
@app.post("/line_msg")
async def post_line_msg(request: Request) -> str:
    """LINE Bot webhook callback
    Args:
        request (Request): Request Object.
    Raises:
        HTTPException: Invalid Signature Error
    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()

    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400,
                            detail="Invalid signature. Please check your channel access token/channel secret.")
    return "OK"


@handler.add(FollowEvent)
def handle_follow(event) -> None:
    """Event - User follow LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    user_event_service.handle_follow(event=event)


@handler.add(UnfollowEvent)
def handle_unfollow(event) -> None:
    """Event - User ban LINE Bot
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    user_event_service.handle_unfollow(event=event)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) -> None:
    """Event - User sent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    message_event_service.handle_message(event=event)


# Admin only
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# Everyone
@app.get("/")
def root_greeting():
    return {"Hello! Here is DoctorJobs"}


@app.get("/msgs/{msg_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
