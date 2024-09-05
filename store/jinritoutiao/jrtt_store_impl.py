'''
File Name: jrtt_store_impl
Create File Time: 2024/5/28 13:57
File Create By Author: Yang Guanqun
Email: yangguanqunit@outlook.com
'''
import csv
import pathlib
from typing import Dict, List

import aiofiles
import tortoise.exceptions

from base.base_crawler import AbstractStore
from tools import utils
from var import crawler_type_var  # 类似全局变量的东西
from tortoise.contrib.pydantic import pydantic_model_creator

class JinritoutiaoCsvStoreImplement(AbstractStore):
    csv_store_path: str = "data/jinritoutiao"

    def make_save_file_name(self, store_type: str) -> str:
        """
        make save file name by store type
        Args:
            store_type: contents or comments

        Returns: eg: data/bilibili/search_comments_20240114.csv ...

        """
        return f"{self.csv_store_path}/{crawler_type_var.get()}_{store_type}_{utils.get_current_date()}.csv"

    async def save_data_to_csv(self, save_item: Dict, store_type: str):
        """
        Below is a simple way to save it in CSV format.
        Args:
            save_item:  save content dict info
            store_type: Save type contains content and comments（contents | comments）

        Returns: no returns

        """
        pathlib.Path(self.csv_store_path).mkdir(parents=True, exist_ok=True)
        save_file_name = self.make_save_file_name(store_type=store_type)
        async with aiofiles.open(save_file_name, mode="a+", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            if await f.tell() == 0:
                await writer.writerow(save_item.keys())
            await writer.writerow(save_item.values())

    async def store_content(self, content_item: Dict):
        """
        Jinritoutiao content CSV storage implementation
        Args:
            content_item: note item dict

        Returns:

        """
        await self.save_data_to_csv(save_item=content_item, store_type="content")

    async def store_comment(self, comment_item: Dict):
        """
        Jinritoutiao comment CSV storage implementation
        Args:
            comment_item: comment item dict

        Returns:

        """
        await self.save_data_to_csv(save_item=comment_item, store_type="comment")


class JinritoutiaoDbStoreImplement(AbstractStore):
    async def store_content(self, content_item: Dict):
        """
        Jinritoutiao content DB storage implementation
        Args:
            content_item: content item dict

        Returns:

        """
        from .jrtt_store_db_types import JinritoutiaoNoteModel
        note_id = content_item.get("note_id")
        if not await JinritoutiaoNoteModel.filter(note_id=note_id).exists():
            content_item["add_ts"] = utils.get_current_timestamp()
            jinritoutiao_note_pydantic = pydantic_model_creator(JinritoutiaoNoteModel, name="JinritoutiaoNoteCreate", exclude=('id',))
            jinritoutiao_data = jinritoutiao_note_pydantic(**content_item)
            jinritoutiao_note_pydantic.model_validate(jinritoutiao_data)
            await JinritoutiaoNoteModel.create(**jinritoutiao_data.model_dump())
        else:
            jinritoutiao_note_pydantic = pydantic_model_creator(JinritoutiaoNoteModel, name="JinritoutiaoNoteUpdate",
                                                                exclude=('id', 'add_ts'))
            jinritoutiao_data = jinritoutiao_note_pydantic(**content_item)
            jinritoutiao_note_pydantic.model_validate(jinritoutiao_data)
            await JinritoutiaoNoteModel.filter(note_id=note_id).update(**jinritoutiao_data.model_dump())

    async def store_comment(self, comment_item):
        """
        Jinritoutiao content DB storage implementation
        Args:
            comment_item_list: comment item dict

        Returns:

        """
        from .jrtt_store_db_types import JinritoutiaoCommentModel

        comment_id = comment_item.get("comment_id", "")
        assert comment_id != "", "[Error] comment id is None..."
        if not await JinritoutiaoCommentModel.filter(comment_id=comment_id).exists():
            comment_item["add_ts"] = utils.get_current_timestamp()
            comment_pydantic = pydantic_model_creator(JinritoutiaoCommentModel, name="JinrotoutiaoNoteCommentCreate",
                                                      exclude=('id',))  # pydantic 库是 python 中用于数据接口定义检查与设置管理的库
            comment_data = comment_pydantic(**comment_item)
            comment_pydantic.model_validate(comment_data)
            await JinritoutiaoCommentModel.create(**comment_data.model_dump())
        else:
            comment_pydantic = pydantic_model_creator(JinritoutiaoCommentModel, name="JinritoutiaoNoteCommentUpdate",
                                                      exclude=('comment_id', 'add_ts'))
            comment_item.pop("comment_id")
            comment_data = comment_pydantic(**comment_item)
            comment_pydantic.model_validate(comment_data)
            await JinritoutiaoCommentModel.filter(comment_id=comment_id).update(**comment_data.model_dump())

    async def store_reply(self, reply_item: Dict):

        from .jrtt_store_db_types import JinritoutiaoReplyModel

        reply_id = reply_item.get("reply_id", "")
        assert reply_id != "", "[Error] reply id is None..."
        if not await JinritoutiaoReplyModel.filter(reply_id=reply_id).exists():
            reply_item["add_ts"] = utils.get_current_timestamp()
            reply_pydantic = pydantic_model_creator(JinritoutiaoReplyModel, name="JinrotoutiaoCommentReplyCreate",
                                                      exclude=('id',))  # pydantic 库是 python 中用于数据接口定义检查与设置管理的库
            reply_data = reply_pydantic(**reply_item)
            reply_pydantic.model_validate(reply_data)
            await JinritoutiaoReplyModel.create(**reply_data.model_dump())
        else:
            reply_pydantic = pydantic_model_creator(JinritoutiaoReplyModel, name="JinrotoutiaoCommentReplyUpdate",
                                                      exclude=('reply_id', 'add_ts'))
            reply_item.pop("reply_id")
            reply_data = reply_pydantic(**reply_item)
            reply_pydantic.model_validate(reply_data)
            await JinritoutiaoReplyModel.filter(reply_id=reply_id).update(**reply_data.model_dump())

    async def fetch_column(self, column_name) -> List[str]:
        from .jrtt_store_db_types import JinritoutiaoIDModel
        note_id_models = await JinritoutiaoIDModel.all().only(f"{column_name}")
        note_ids = []
        for id_ in note_id_models:
            note_ids.append(id_.note_id)

        return note_ids