from contextlib import asynccontextmanager
from core.models import Base, db_helper
import uvicorn
from fastapi import FastAPI
from api_v1 import router as route_v1
from core.config import setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=route_v1, prefix=setting.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8088, reload=True, workers=4)
