from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image

from MaterialEdit.router_百度网盘操作 import router_百度网盘删除和获取链接
from Router import router as router_素材编辑
from router_打开百度网盘下载链接 import router as router_打开百度网盘下载链接

Image.MAX_IMAGE_PIXELS = None
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_素材编辑)
app.include_router(router=router_打开百度网盘下载链接)
app.include_router(
    router=router_百度网盘删除和获取链接.router, prefix="/baiduyun_del_share_request"
)

static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
