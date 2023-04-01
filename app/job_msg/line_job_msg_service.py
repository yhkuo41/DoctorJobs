from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models.events import MessageEvent

from app.db.database import get_db
from app.job_msg import service
from app.job_msg.line_msg_query import LineMsgQuery


async def handle_message(event: MessageEvent, line_bot_api: LineBotApi) -> None:
    query = LineMsgQuery(event.message.text)
    res = []
    if query.error_msgs:
        res.append(TextSendMessage(text=query.pretty_error_msgs()))
    else:
        request = query.to_query_request()
        job_msgs = await service.get_job_msgs(request, next(get_db()).job_msg)
        for job_msg in job_msgs:
            res.append(TextSendMessage(text=job_msg.pretty_msg()))

    if not res:
        res.append(TextSendMessage(text="查無職缺訊息"))

    line_bot_api.reply_message(reply_token=event.reply_token, messages=res[:5])
