import os
import re
import httpx
from bs4 import BeautifulSoup
from note_typing import NoteType

"""
eg:
    2024年超长期特别国债（五期）（以下简称本期国债）已完成招标工作。根据国债发行有关规定，现将有关事项公告如下：
　　    一、本期国债计划发行450亿元，实际发行面值金额450亿元。
　　    二、本期国债期限20年，经招标确定的票面利率为2.33%，2024年8月15日开始计息，招标结束后至8月15日进行分销，8月19日起上市交易。
　　    三、本期国债为固定利率附息债，利息按半年支付，利息支付日为每年的2月15日（节假日顺延，下同）、8月15日，2044年8月15日偿还本金并支付最后一次利息。
　　其他事宜按《国债业务公告》（2024年第2号）规定执行。
　　特此公告。  
"""

re_regular = '国债业务公告[0-9]+年第[0-9]+号'
website_url = "https://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/"

# with httpx.Client() as client:
#     response = client.request(
#         "GET", website_url
#     )
#
#
# soup = BeautifulSoup(response.text, "html.parser")
# all_links = soup.find_all("a")
# for link in all_links:
#     link_title = link.get('title')
#     if link_title is None:
#         continue
#     if re.match(re_regular, link_title) is not None:
#         link_href = link.get('href')
#         item_url = os.path.join(website_url, link_href[2:])
#         print(item_url)
#
#


def parse_note_page(note_page_url: str, note_typing: NoteType):
    with httpx.Client() as client:
        response = client.request(
            "GET", note_page_url
        )
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", {'class': 'Custom_UnionStyle'})
        content_text = content_div.text.strip()
        lines = content_text.split('\n')
        year = re.findall('\s*\d+', lines[0])[0]
        title = re.findall('(?<=年).*?国债', lines[0])[0][1:-1]
        if note_typing == NoteType.LongDurationNote or note_typing == NoteType.InterestNote:
            plan_amount = re.findall('(?<=发行)\d*.+?(?=元)', lines[1])[0]
        actual_amount = re.findall('(?<=面值金额)\d*.+(?=元)', lines[1])[0]

        duration = re.findall('(?<=期限)\d*.+?(?<=[年月天])', lines[2])[0]
        interest_rate = re.findall('(?<=利率为)\d*.+?(?<=[%])',  lines[2])[0]
        interest_start_time = re.findall('\d+年\d+月\d+日(?=开始计息)',  lines[2])[0]







parse_note_page("https://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/202408/t20240814_3941796.htm", NoteType.LongDurationNote)



