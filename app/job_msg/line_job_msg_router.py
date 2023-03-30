from pprint import pprint

from fastapi import APIRouter
from fastapi import HTTPException, Request
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from linebot.models.events import UnsendEvent

from app import config
from app.job_msg import line_job_msg_service

job_msg_line_router = APIRouter(tags=["Job Message (LineBot)"])

handler = WebhookHandler(config.get_secret("LINE_CHANNEL_SECRET"))


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
    pprint(vars(event))
    """Event - User unsent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unsend-event
    """
    line_job_msg_service.handle_unsend(event=event)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) -> None:
    pprint(vars(event))
    """Event - User sent message
    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    line_job_msg_service.handle_message(event=event)
