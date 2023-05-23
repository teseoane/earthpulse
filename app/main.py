from fastapi import FastAPI

from app.routers import sentinel_router

app = FastAPI()
app.include_router(sentinel_router, prefix='/api/v1')


@app.get('/healthcheck')
async def healthcheck():
    return {'status': 'ok'}
