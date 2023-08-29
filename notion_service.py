import os
import re
from dotenv import load_dotenv
from notion_client import Client
from typing import Dict, Any, List


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


# Initialize Notion client
load_dotenv()
notion = Client(auth=os.environ.get('NOTION_API_KEY'))
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


def append_block(block_id: str, text: str, file_type: str, file_url: str, link_list: List[tuple]) -> None:
    new_block_type = "bulleted_list_item"
    new_block = [
        {
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
        },
        {
            "object": "block",
            "type": new_block_type,
            new_block_type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                        }
                    }
                ]
            }
        }
    ]
    if link_list:
        last_start = 0
        last_end = 0
        new_block[1][new_block_type]["rich_text"] = [
            {"type": "text", "text": {"content": text.split(' - ')[0] + " - "}}]
        text = ' - '.join(text.split(' - ')[1:])
        for start, end, content, url in link_list:
            new_block[1][new_block_type]["rich_text"].append(
                {"type": "text", "text": {"content": text[last_end:start]}})
            new_block[1][new_block_type]["rich_text"].append(
                {"type": "text", "text": {"content": content, "link": {"url": url}}})
            last_end = end
        new_block[1][new_block_type]["rich_text"].append({"type": "text", "text": {"content": text[last_end:]}})

    if file_url:
        if "image" in file_type:
            new_block.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        elif "video" in file_type:
            new_block.append({
                "object": "block",
                "type": "video",
                "video": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        elif "audio" in file_type:
            new_block.append({
                "object": "block",
                "type": "audio",
                "audio": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        else:
            new_block.append({
                "object": "block",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
    notion.blocks.children.append(block_id, children=new_block, after=False)


def update_block(page_id: str, text: str, file_type: str, file_url: str,
                 link_list: List[tuple]) -> None:
    content = get_page_content(page_id)
    block_id = content["results"][-1]["id"]
    append_block(block_id, text, file_type, file_url, link_list)


def insert(text: str = "", file_type: str = "", file_url: str = "", link_list=None) -> None:
    # update_block(page_id, text, file_type, file_url, link_list)
    if link_list is None:
        link_list = []
    print(locals())
    append_block(page_id, text, file_type, file_url, link_list)


if __name__ == "__main__":
    # update_block(page_id, "test", None, None, None)
    append_block(page_id, "test", None, None, [(1, 2, "小仓库", 'https://t.me/storage_qi/62')])
    get_page_content(page_id)
    # create_page("test", "12", "34")
    # insert("你感觉怎么样")
