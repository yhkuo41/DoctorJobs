from bson import ObjectId
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models.events import UnsendEvent, MessageEvent

from app.db.database import get_db
from app.job_msg import msg_filter, service
from app.job_msg.schema import JobMsgPutRequest


async def handle_message(event: MessageEvent, line_bot_api: LineBotApi) -> None:
    if len(event.message.text) < 20:  # 忽視短訊息，避免JobMsgPutRequest驗證失敗
        return
    # get_job_msg_by_id
    if len(event.message.text) == 24 and ObjectId.is_valid(event.message.text):
        job_msg = await service.get_job_msg_by_id(event.message.text, next(get_db()).job_msg)
        if job_msg:
            res = job_msg.pretty_msg()
        else:
            res = "查無職缺訊息"
        line_bot_api.reply_message(reply_token=event.reply_token,
                                   messages=TextSendMessage(text=res))
        return

    # upsert
    req = JobMsgPutRequest(raw_msg=event.message.text, line_msg_id=event.message.id)
    await service.tag_if_needed(req, raise_error=False)
    not_recruitment = any(not f.apply(req) for f in msg_filter.filters)
    if not_recruitment:
        return

    try:
        res = await service.find_duplicate_then_upsert(req, next(get_db()).job_msg, event.source.user_id)
    except Exception as e:
        res = str(e)

    line_bot_api.reply_message(reply_token=event.reply_token,
                               messages=TextSendMessage(text=f"Upsert success, job_msg_id: {res}"))


async def handle_unsend(event: UnsendEvent) -> None:
    # unsend沒有reply_token
    await service.delete_job_msg_by_line_msg_id(event.unsend.message_id,
                                                event.source.user_id,
                                                next(get_db()).job_msg)
