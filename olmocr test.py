# This was for testing and it's not used

from openai import OpenAI
import asyncio
import multiprocessing

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=600)

from pprint import pprint
from olmocr.pipeline import build_page_query


async def main():
    query = await build_page_query("test.pdf",
                                page=4,
                                target_longest_image_dim=1024,
                                target_anchor_text_len=6000)

    query['model'] = 'allenai_olmocr-7b-0225-preview'

    response = client.chat.completions.create(**query)

    print(response.choices[0].message.content)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    asyncio.run(main())
