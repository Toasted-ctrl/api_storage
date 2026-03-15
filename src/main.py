from fastapi import FastAPI

from api.v1 import user, data, status, root
from core.config import config

v1_prefix = "/api/v1"

app = FastAPI(title=config.app_name,
              version=config.app_version)

app.include_router(root.router, prefix=v1_prefix)
app.include_router(user.router, prefix=v1_prefix)
app.include_router(data.router, prefix=v1_prefix)
app.include_router(status.router, prefix=v1_prefix)