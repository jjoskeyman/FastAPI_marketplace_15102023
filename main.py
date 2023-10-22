from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import setting
from core.models import db_helper, Base


# from core.models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as connection:
    #     await connection.run_sync(Base.metadata.drop_all)
    #     await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=setting.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True, workers=4)
