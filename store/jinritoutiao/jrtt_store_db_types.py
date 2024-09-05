'''
File Name: jrtt_store_db_types
Create File Time: 2024/5/28 10:48
File Create By Author: Yang Guanqun
Email: yangguanqunit@outlook.com
'''

"""Object Relational Mapping(对象关系映射)，把对象当作数据库来使用"""
from tortoise import fields
from tortoise.models import Model


class JinritoutiaoIDModel(Model):
    id = fields.IntField(pk=True, autoincrement=True, description="自增ID")
    note_id = fields.CharField(null=False, max_length=20, description="note guid")
    class Meta:
        table = "NoteID"
        table_description = "store all the notes id in NoteID"


class JinritoutiaoBaseModel(Model):
    note_id = fields.CharField(null=False, max_length=20, description="note guid")
    user_id = fields.CharField(null=False, max_length=20, description="user guid")
    user_name = fields.CharField(null=False, max_length=30, description="user name")
    ip_location = fields.CharField(null=True, max_length=10, description="user ip location")
    add_ts = fields.BigIntField(description="timestamp")
    create_time = fields.BigIntField(description="comment timestamp", index=True)  # 评论时间戳

    class Meta:
        abstract = True


class JinritoutiaoNoteModel(JinritoutiaoBaseModel):
    content = fields.TextField(null=True, description="note content")  # 帖子正文内容
    create_time = fields.BigIntField(description="note timestamp", index=True)  # 帖子发布时间戳
    create_data_time = fields.CharField(max_length=32, description="note date", index=True)  # 帖子发布日期 index 可能是按某种顺序存储？
    liked_count = fields.CharField(null=True, max_length=16, description="liked count")  # 帖子点赞数
    comments_count = fields.CharField(null=True, max_length=16, description="comments count")  # 帖子评论数量
    shared_count = fields.CharField(null=True, max_length=16, description="transmits count")  # 帖子转发数量
    note_url = fields.CharField(null=True, max_length=512, description="note url")  # 帖子详情URL

    class Meta:
        table = "jinritoutiao_note"
        table_description = "今日头条帖子"

    def __str__(self):
        return f"{self.note_id}"


class JinritoutiaoCommentModel(JinritoutiaoBaseModel):
    comment_id = fields.CharField(null=False, pk=True, max_length=20, index=True, description="comment guid")  # 评论id
    text = fields.TextField(null=False, description="comment content")  # 评论内容
    reply_count = fields.IntField(null=True, description="account for replying this comment")
    create_time = fields.BigIntField(description="comment timestamp", index=True)  # 评论时间戳
    # create_data_time = fields.CharField(max_length=32, description="comment date", index=True)  # 评论日期 index 可能是按某种顺序存储？
    # comment_like_count = fields.CharField(max_length=16, description="like count")  # 评论点赞数
    # sub_comment_count = fields.CharField(max_length=16, description="sub comment count")  # 评论回复数

    class Meta:
        table = "jinritoutiao_note_comment"
        table_description = "今日头条帖子评论"

    def __str__(self):
        return f"{self.comment_id}"


class JinritoutiaoReplyModel(JinritoutiaoBaseModel):
    reply_id = fields.CharField(null=False, pk=True, max_length=20, index=True, description="reply guid")
    comment_id = fields.CharField(null=False, max_length=20, index=True, description="comment guid")  # 评论id
    text = fields.TextField(null=False, description="reply content")  # 评论内容
    to_reply = fields.BooleanField(null=False, description="a reply to comment or reply, false is reply to comment")
    to_reply_id = fields.CharField(null=True, max_length=20, index=True, description="reply to a reply id if to_reply is true")

    class Meta:
        table = "jinritoutiao_note_comment_reply"
        table_description = "今日头条评论回复"

    def __str__(self):
        return f"{self.reply_id}"
