'''
File Name: __init__.py
Create File Time: 2024/5/28 10:38
File Create By Author: Yang Guanqun
Email: yangguanqunit@outlook.com
'''

import config

from .jrtt_store_db_types import *
from .jrtt_store_impl import *


class JinritoutiaostoreFactory:
    STORES = {
        "csv": JinritoutiaoCsvStoreImplement,
        "db": JinritoutiaoDbStoreImplement,
        "json": None
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = JinritoutiaostoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[JinritoutiaoFactory.create_store] Invalid save option only supported csv or db or json ..."
            )
        return store_class()


async def update_jinritoutiao_note(note_item: Dict):
    note_id = note_item.get("note_id")

    local_db_item = {
        "note_id": note_item.get("note_id"),
        "type": note_item.get("type"),
        "user_id": note_item.get("user_id"),
        "user_name": note_item.get("user_name"),
        "timestamp": note_item.get("create_time"),
        "ip_location": note_item.get("ip_location"),
        "content": note_item.get("text"),
        "comment_count": note_item.get("comment_count")
    }

    utils.logger.info(
        f"[store.jinritoutiao.udpate_jinritoutiao_note] jinritoutiao note id: {note_id}, note: {local_db_item}"
    )
    await JinritoutiaostoreFactory.create_store().store_content(local_db_item)


async def batch_update_jinritoutiao_note_comments(note_id: str, comments: List[Dict]):
    if not comments:
        return
    for comment in comments:
        await update_jinritoutiao_note_comment(note_id, comment)

async def batch_update_jinritoutiao_comment_replies(note_id, replies: List[Dict]):
    if not replies:
        return
    for reply in replies:
        await update_jinritoutiao_comment_reply(note_id, reply)


async def update_jinritoutiao_note_comment(note_id: str, comment_item):
    comment_id: str = str(comment_item.get("comment_id"))
    local_db_item = {
        "comment_id": comment_id,
        "note_id": note_id,
        "user_id": comment_item.get("user_id"),
        "user_name": comment_item.get("user_name"),
        "ip_location": comment_item.get("ip_location"),
        "create_time": comment_item.get("create_time"),
        "reply_count": comment_item.get("reply_count"),
        "text": comment_item.get("text"),
    }

    utils.logger.info(
        f"[store.jinritoutiao.update_jinritoutiao_note_comment] Jinritoutiao note comment: {local_db_item}"
    )
    await JinritoutiaostoreFactory.create_store().store_comment(local_db_item)


async def update_jinritoutiao_comment_reply(note_id: str, reply_item: Dict):
    comment_id: str = str(reply_item.get("comment_id"))
    reply_id: str = str(reply_item.get("reply_id"))
    local_db_item = {
        "reply_id": reply_id,
        "note_id": note_id,
        "comment_id": comment_id,
        "user_id": reply_item.get("user_id"),
        "user_name": reply_item.get("user_name"),
        "ip_location": reply_item.get("ip_location"),
        "to_reply": reply_item.get("to_reply"),
        "to_reply_id": reply_item.get("to_reply_id"),
        "text": reply_item.get("text"),
        "create_time": reply_item.get("create_time"),
    }

    utils.logger.info(

        f"[store.jinritoutiao.update_jinritoutiao_comment_reply] Jinritouriao comment reply: {local_db_item}"
    )
    await JinritoutiaostoreFactory.create_store().store_reply(local_db_item)


async def get_jinritoutiao_note_id(column="note_id") -> List[str]:
    column_values = await JinritoutiaostoreFactory.create_store().fetch_column(column)
    return column_values
