#--- import DB to initialize it
from tinypip import tinydb

#--- initialize main FastAPI instance
from fastapi import FastAPI

app = FastAPI()

from tinypip.api import main_router

app.include_router(main_router.router)


@app.get("/")
async def root():
    return {
        "message": "Yeetus"
    }


if __name__ == '__main__':
    from uvicorn.config import Config
    from uvicorn.server import Server

    config = Config(
        'tinypip.__main__:app',
        port=8000,
        log_level='debug',
        reload=False,
        host='0.0.0.0',
        forwarded_allow_ips='*'
    )
    try:
        server = Server(config)
        server.run()
    except KeyboardInterrupt:
        pass
