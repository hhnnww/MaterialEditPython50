from fastapi import APIRouter
from requests_html import HTMLSession
from fastapi.responses import Response

router = APIRouter(prefix="/img")


@router.get("/get_url")
def get_url(img_url: str):
    print(img_url)
    session = HTMLSession()
    res = session.get(img_url).content
    return Response(res, media_type="image/png")
