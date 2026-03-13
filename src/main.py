from fastapi import FastAPI

from src.api.v1 import user, data, status, root
#from app.database2.schema import Base
#from app.database2.session import engine

#Base.metadata.create_all(bind=engine)

v1_prefix = "/api/v1"

app = FastAPI()

app.include_router(root.router, prefix=v1_prefix)
app.include_router(user.router, prefix=v1_prefix)
app.include_router(data.router, prefix=v1_prefix)
app.include_router(status.router, prefix=v1_prefix)