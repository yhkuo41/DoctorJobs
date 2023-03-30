from linebot import LineBotApi
from linebot.models import SourceGroup, SourceUser, TextSendMessage
from linebot.models.events import UnsendEvent, MessageEvent

from app import config

line_bot_api = LineBotApi(config.get_secret("LINE_CHANNEL_ACCESS_TOKEN"))


def handle_message(event: MessageEvent) -> None:
    reply_token = event.reply_token
    # {'delivery_context': {"isRedelivery": false},
    #  'message': {"id": "17862804526478", "text": "test", "type": "text"},
    #  'mode': 'active',
    #  'reply_token': '5788dfe8351344be93f64de44c24e6f9',
    #  'source': {"groupId": "Cfb9876a9c5fd13363ed71e868b8992f0", "type": "group",
    #             "userId": "U138383ec9583e853cb6859090b5e6745"},
    #  'timestamp': 1679720045172,
    #  'type': 'message',
    #  'webhook_event_id': '01GWBHVPPFXYJ5D661RK3XXQCK'}

    if isinstance(event.source, SourceGroup):
        pass
    elif isinstance(event.source, SourceUser):
        pass
    # Get user sent message
    user_message = event.message.text * 50

    # Reply with same message
    messages = [TextSendMessage(text=user_message), TextSendMessage(text=user_message),
                TextSendMessage(text=user_message), TextSendMessage(text=user_message),
                TextSendMessage(text=user_message)]
    line_bot_api.reply_message(reply_token=reply_token, messages=messages)


def handle_unsend(event: UnsendEvent) -> None:
    # {'delivery_context': {"isRedelivery": false},
    #  'mode': 'active',
    #  'source': {"groupId": "Cfb9876a9c5fd13363ed71e868b8992f0", "type": "group",
    #             "userId": "U138383ec9583e853cb6859090b5e6745"},
    #  'timestamp': 1679720375450,
    #  'type': 'unsend',
    #  'unsend': {"messageId": "17862794185910"},
    #  'webhook_event_id': '01GWBJ5S79K6S7HSR2Q880NNGT'}
    pass
