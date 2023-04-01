import asyncio
from pprint import pprint

from fastapi import APIRouter
from fastapi import HTTPException, Request
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, SourceGroup, SourceUser
from linebot.models.events import UnsendEvent

from app import config
from app.job_msg import line_job_msg_service, line_admin_group_service

job_msg_line_router = APIRouter(tags=["Job Message (LineBot)"])

handler = WebhookHandler(config.get_secret("LINE_CHANNEL_SECRET"))
line_bot_api = LineBotApi(config.get_secret("LINE_CHANNEL_ACCESS_TOKEN"))
admin_group_id = config.get_secret("LINE_ADMIN_GROUP_ID")


@job_msg_line_router.post("/job_msg_line")
async def post_job_msg_by_line(request: Request) -> str:
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


@handler.add(UnsendEvent)
def handle_unsend(event) -> None:
    event.message.text = event.message.text.strip()
    pprint(vars(event))
    """Event - User unsent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unsend-event
    """
    if isinstance(event.source, SourceGroup) and event.source.group_id == admin_group_id:
        asyncio.create_task(line_admin_group_service.handle_unsend(event=event, line_bot_api=line_bot_api))


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event) -> None:
    """Event - User sent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    event.message.text = event.message.text.strip()
    pprint(vars(event))
    if event.message.text.lower() == "help":
        return
    if isinstance(event.source, SourceGroup):
        if event.source.group_id == admin_group_id:
            asyncio.create_task(line_admin_group_service.handle_message(event=event, line_bot_api=line_bot_api))
    elif isinstance(event.source, SourceUser):
        asyncio.create_task(line_job_msg_service.handle_message(event=event, line_bot_api=line_bot_api))
