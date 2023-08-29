import ast
import datetime
import os
import re
from pprint import pprint

from dotenv import load_dotenv
from notion_client import Client
from typing import Dict, Any, Optional


def get_page_id_from_url(url: str) -> str:
    """
    从页面url中获取页面id
    :param url:
    :return:
    """
    id_regex = re.compile(r'([\w|\d]{32}$)')
    id_raw = id_regex.findall(url)[0]
    id_processed = '-'.join([
        id_raw[0:8], id_raw[8:12], id_raw[12:16], id_raw[16:20], id_raw[20:]])
    return id_processed


load_dotenv()
# Initialize Notion client
notion = Client(auth=os.environ.get('NOTION_API_KEY'))
PAGE_TITLE_MAX_LENGTH = int(os.environ.get('BOOKMARK_TITLE_MAX_LENGTH'))
# Define database ID
page_id = get_page_id_from_url("853d0afe2d5c4fd5a55994b9bcf07b1c")


def get_page_content(page_id: str) -> Dict[str, Any]:
    """
    Retrieve the content of a page with the given page_id.

    :param page_id: The ID of the page whose content is to be retrieved.
    :return: A dictionary containing information about the page's content.
    """
    content = notion.blocks.children.list(page_id)
    # pprint(content)
    return content


def append_block(add_block) -> None:
    notion.blocks.children.append(page_id, children=add_block, after=False)


def generate_heading_block(heading_type: int = 1, *args) -> dict:
    heading = f"heading_{heading_type}"
    return {
        "type": heading,
        heading: {
            "rich_text": [content for content in args],
        }
    }


def generate_blank_block() -> Dict:
    return {
        # 空行
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": ""
                    }
                }
            ]
        }
    }


def generate_divider_block() -> Dict:
    new_block_type = "divider"
    return {
        "object": "block",
        "type": new_block_type,
        new_block_type: {}
    }


def generate_link_text_block(content: str, link: str) -> dict:
    new_block_type = "text"
    return {
        "type": new_block_type,
        new_block_type: {
            "content": content,
            "link": {"url": link}
        },
    }


def generate_text_block(content: str) -> dict:
    new_block_type = "text"
    return {
        "type": new_block_type,
        new_block_type: {
            "content": content,
        },
    }


def generate_date_text_block(start_date: datetime) -> dict:
    new_block_type = "mention"
    return {
        "type": new_block_type,
        new_block_type: {
            "type": "date",
            "date": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": None,
            }
        },
    }


def generate_bookmark_block(text: Optional[str], link: str) -> dict:
    title = text if len(
        text) < PAGE_TITLE_MAX_LENGTH else text[:PAGE_TITLE_MAX_LENGTH] + '...'
    new_block_type = "bookmark"
    return {
        "object": "block",
        "type": new_block_type,
        new_block_type: {
            "caption": [
                {
                    "type": "text",
                    "text": {
                        "content": title,
                    },
                }
            ],
            "url": link,
        }
    }


if __name__ == "__main__":
    txt = """[{'heading_1': {'rich_text': [{
                               'text': {'content': 'SM AV 小仓库',
                                        'link': {'url': 'https://t.me/SM_AV1'}},
                               'type': 'text'},
                              {'mention': {'date': {'end': None,
                                                    'start': '2023-08-29'},
                                           'type': 'date'},
                               'type': 'mention'}]},
  'type': 'heading_1'},
 {'bookmark': {'caption': [],
               'url': 'https://t.me/SM_AV1/86'},
  'object': 'block',
  'type': 'bookmark'}]"""

    data = ast.literal_eval(txt)
    append_block(data)
    # pprint(get_page_content(page_id))
