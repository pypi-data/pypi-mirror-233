from . import escape_html, escape_markdown


def bold(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to bold format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<b>{text if escape is False else escape_html(text)}</b>"
    else:
        return f"*{text if escape is False else escape_markdown(text)}*"


def italic(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to italic format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<i>{text if escape is False else escape_html(text)}</i>"
    else:
        return f"_{text if escape is False else escape_markdown(text)}_"


def underline(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to underline format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<u>{text if escape is False else escape_html(text)}</u>"
    else:
        return f"__{text if escape is False else escape_markdown(text)}__"


def strikethrough(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to strikethrough format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<s>{text if escape is False else escape_html(text)}</s>"
    else:
        return f"~{text if escape is False else escape_markdown(text)}~"


def spoiler(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to spoiler format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f'<span class="tg-spoiler">{text if escape is False else escape_html(text)}</span>'
    else:
        return f"||{text if escape is False else escape_markdown(text)}||"


def hyperlink(text: str, url: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to hyperlink format

    Args:
        text (``str``):
            The hyperlink text

        url (``str``):
            The hyperlink url

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    assert isinstance(url, str), "url must be str"

    if html:
        return f'<a href="{url}">{text if escape is False else escape_html(text)}</a>'
    else:
        return f"[{text if escape is False else escape_markdown(text)}]({url})"


def mention(text: str, user_id: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to inline mention format

    Args:
        text (``str``):
            The text of inline mention

        user_id (``str``):
            The inline user id to mention

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f'<a href="tg://user?id={user_id}">{text if escape is False else escape_html(text)}</a>'
    else:
        return f"[{text if escape is False else escape_markdown(text)}](tg://user?id={user_id})"


def custom_emoji(emoji: str, custom_emoji_id: int, html: bool = False) -> str:
    """Convert the given emoji to custom emoji format

    Args:
        emoji (``str``):
            The emoji of the custom emoji

        custom_emoji_id (``str``):
            Identifier of the custom emoji

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji}</tg-emoji>'
    else:
        return f"![{emoji}](tg://emoji?id={custom_emoji_id})"


def code(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to code format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<code>{text if escape is False else escape_html(text)}</code>"
    else:
        return f"`{text if escape is False else escape_markdown(text)}`"


def pre(text: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to pre format

    Args:
        text (``str``):
            The text to convert

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    if html:
        return f"<pre>{text if escape is False else escape_html(text)}</pre>"
    else:
        return f"```\n{text if escape is False else escape_markdown(text)}\n```"


def pre_code(text: str, language: str, html: bool = False, escape: bool = True) -> str:
    """Convert the given text to pre code format

    Args:
        text (``str``):
            The text to convert

        language (``str``):
            The name of the programming language written in the given code block

        html (``bool``, *optional*):
            Pass ``True`` to return text in ``html`` format. Default is ``False`` (``markdownv2``)

        escape (``bool``, *optional*):
            Whether escape special characters to the given text or not. Default is ``True``

    Returns:
        :py:class:`str`: The formated text
    """

    assert isinstance(language, str), "text must be str"

    if html:
        return f'<pre><code class="language-{language}">{text if escape is False else escape_html(text)}</code></pre>'
    else:
        return (
            f"```{language}\n{text if escape is False else escape_markdown(text)}\n```"
        )
