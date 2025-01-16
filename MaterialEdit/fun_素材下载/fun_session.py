"""."""

from requests_html import HTML, HTMLSession


def fun_session(url: str, cookie: str) -> HTML:
    """."""
    session = HTMLSession()

    with session.get(
        url=url,
        headers={
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",  # noqa: E501
        },
    ) as res:
        html: HTML = res.html  # type: ignore  # noqa: PGH003
    return html
