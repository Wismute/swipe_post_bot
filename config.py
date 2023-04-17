"""Конфигурация и основные тексты"""


HELLO_TEXT = """
**Привет, {}!**

Здесь ты можешь просматривать посты и переходить между ними, используя кнопки.

Enjoy!
"""


async def create_post_text(post: dict, all_posts_count: int) -> str:
    """Форматирование текста поста"""

    return f"""
        **{post['title'].title()}**

        {post['body'].title()}

        __{post['id']}/{all_posts_count}__

        """.replace('    ', '')
