# 安装

```
set https_proxy=http://192.168.0.110:7890
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv run uvicorn main:app

powershell -ExecutionPolicy ByPass -c "irm Z:\DOWN\uv-installer.ps1 | iex"

```
