from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.gzip import GZipMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.rate_limiter import limiter
from app.api import api_router
from app.plugins.app_nacos.service import send_heartbeats, stop_heartbeats


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )


exception_handlers = {404: not_found}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await send_heartbeats()
    yield
    await stop_heartbeats()


# we create the ASGI for the app
app = FastAPI(exception_handlers=exception_handlers, openapi_url="")
# app = FastAPI(exception_handlers=exception_handlers, openapi_url="", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# we create the Web API framework
api = FastAPI(
    title="App",
    description="Welcome to App's API documentation! Here you will able to discover all of the ways you can interact with the App API.",
    root_path="/api/v1",
    docs_url="/docs",
    openapi_url="/docs/openapi.json",
    redoc_url="/redocs",
)
api.add_middleware(GZipMiddleware, minimum_size=1000)

# we add all API routes to the Web API framework
api.include_router(api_router)

app.mount("/api/v1", app=api)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
