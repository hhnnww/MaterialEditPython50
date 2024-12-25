"""素材编辑程序."""

import logging
from pathlib import Path

from colorama import Fore, Style
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image

from MaterialEdit.router_百度网盘操作 import router_百度网盘删除和获取链接
from route_上传到百度网盘.route import route as route_上传到百度网盘
from Router import router as router_素材编辑
from router_chrome_plugin.router import router as router_chrome_plugin
from router_打开百度网盘下载链接 import router as router_打开百度网盘下载链接

Image.MAX_IMAGE_PIXELS = None
app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format=f"{Fore.YELLOW}%(levelname)s{Style.RESET_ALL}:\t%(asctime)s - %(message)s",
)


origins = ["*"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=route_上传到百度网盘)
app.include_router(router=router_素材编辑)
app.include_router(router=router_打开百度网盘下载链接)
app.include_router(
    router=router_百度网盘删除和获取链接.router,
    prefix="/baiduyun_del_share_request",
)
app.include_router(router=router_chrome_plugin)

static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
