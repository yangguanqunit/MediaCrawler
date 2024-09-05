from bs4 import BeautifulSoup
import nest_asyncio
from tortoise import fields
from tortoise.models import Model
import asyncio
from tortoise import Tortoise, run_async
import re

# # Step 1: Open and read the HTML file
with open('page_source.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'lxml')  # You can use 'html.parser' instead of 'lxml' if needed

# title = soup.title.text
# print(f"Page Title: {title}")


content_id = soup.find_all("p", class_="content")

# for id in content_id:
#     res = re.sub("#.*#", "", id.text)
#     print()

nest_asyncio.apply()  # Allow nested event loops

class NoteID(Model):
    id = fields.IntField(pk=True, autoincrement=True, description="自增ID")
    note_id = fields.CharField(null=False, max_length=20, description="note guid")

    class Meta:
        table = "NoteID"
        table_description = "store all the notes id in NoteID"

class NoteContentModel(Model):
    note_id = fields.CharField(null=False, max_length=20, pk=True, description='note guid')
    text = fields.TextField(null=True, description="store the concrete content of corresponding note id")

    class Meta:
        table = "NoteContentTable"
        table_description = "the table to store note id and its corresponding note content"

async def init():
    await Tortoise.init(
        db_url='mysql://ygq:ygq@172.27.54.34:3306/Crawler',
        modules={'models': ['__main__']}  # Adjust as necessary
    )
    await Tortoise.generate_schemas()
#
async def launch():
    await init()

    # # only add note id
    note_id_to_create = [
        NoteID(note_id=f"{id.a.get('href').split('/')[-2]}") for id in reversed(content_id)
    ]
    await NoteID.bulk_create(note_id_to_create)
    print("Inserted NoteID in batch.")

    note_content_to_create = [
        NoteContentModel(note_id=f"{id.a.get('href').split('/')[-2]}", text=f'{re.sub("#.*#", "", id.text)}') for id in reversed(content_id)
    ]
    await NoteContentModel.bulk_create(note_content_to_create)

    await Tortoise.close_connections()
#
# # Directly await the launch function
#
# # async def launch():
# #     await init()
# #     items = await NoteID.all().only("123")
# #     for item in items:
# #         print(item.note_id)
# #
# #     await Tortoise.close_connections()
#
asyncio.run(launch())



