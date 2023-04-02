from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fligt_service.api.routers.flight_router import router

app = FastAPI(
    title="S7Test",
    version="0.1Alpha",
    description="Получение рейсов",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # так не делать в проде, но для докера сойдет
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)