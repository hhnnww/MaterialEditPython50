from fastapi import APIRouter
from fastapi.responses import Response
from requests_html import HTMLSession

router = APIRouter(prefix="/img")


@router.get("/get_url")
def get_url(img_url: str):
    print(img_url)
    session = HTMLSession()
    res = session.get(img_url).content
    return Response(res, media_type="image/png")
