from linebot import LineBotApi
from linebot.models.events import UnsendEvent, MessageEvent


async def handle_message(event: MessageEvent, line_bot_api: LineBotApi):
    return None


async def handle_unsend(event: UnsendEvent, line_bot_api: LineBotApi) -> None:
    # {'delivery_context': {"isRedelivery": false},
    #  'mode': 'active',
    #  'source': {"groupId": "Cfb9876a9c5fd13363ed71e868b8992f0", "type": "group",
    #             "userId": "U138383ec9583e853cb6859090b5e6745"},
    #  'timestamp': 1679720375450,
    #  'type': 'unsend',
    #  'unsend': {"messageId": "17862794185910"},
    #  'webhook_event_id': '01GWBJ5S79K6S7HSR2Q880NNGT'}
    pass
