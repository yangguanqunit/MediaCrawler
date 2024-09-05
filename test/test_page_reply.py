import asyncio

from media_platform.jinritoutiao import JrttClient
from tools import utils

cooke_str = "__ac_signature=_02B4Z6wo00f01mU1aSQAAIDDbxOyj4CBN.plFW2AAPxK9a; tt_webid=7311151821980190235; ttcid=505172fabf3f420a9c17ecb9265b7bda25; csrftoken=23ef8f85aedaf4a2f666f49fab77be18; _ga=GA1.1.1830206250.1702260199; s_v_web_id=verify_lvafozo9_klyHfxxS_jP3U_4I9q_9L7S_WQPcjqZFkTvI; passport_csrf_token=2c3452e681bae2d033a9495e752db658; passport_csrf_token_default=2c3452e681bae2d033a9495e752db658; local_city_cache=%E6%9D%AD%E5%B7%9E; _S_WIN_WH=1920_919; _S_DPR=1; _S_IPAD=0; gfkadpd=24,6457; __feed_out_channel_key=entertainment; msToken=JmGxMcXm2OkcKeo7pVnIVoNv7_97lz1Nea6Fo6uDsjbV5gM7wc-fIY7ApMF8R0dggUiQbGOHOSFi3i078MO5KsYC6tf_CRRWTOp0EPk5; _ga_QEHZPBE5HH=GS1.1.1717125380.229.1.1717125692.0.0.0; tt_scid=wUOXrbo4LRaktH.7F1MLVi9fkAosZZTF1awf0H4-scIx8o97ogA2Gf-txRM7Glka19d4; ttwid=1%7CYyHTdScUsMQhb5LrPuAH1qd_Vbgaeyrah34TnCQFQ54%7C1717125692%7C8de32aacea65d3ee982422d7615e6fdc101cd4e0a6bf105849de19ddb13d76a0"

jrtt_client_obj = JrttClient(
            proxies=None,
            headers={
                "User-Agent": utils.get_user_agent(),
                "Cookie": cooke_str,
                "Host": "www.toutiao.com",
                "Origin": "https://www.toutiao.com/",
                "Referer": "https://www.toutiao.com/",
                "Content-Type": "application/json;charset=UTF-8"
            },
            playwright_page=None,
            cookie_dict=utils.Cookie,
        )

async def run():
    res = await jrtt_client_obj.get_comment_all_replies("7409914998660612899")
    return res
asyncio.run(run())