#--- import DB to initialize it
from tinypip import tinydb

#--- initialize main FastAPI instance
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    import logging

    logging.getLogger().setLevel(logging.DEBUG)

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
