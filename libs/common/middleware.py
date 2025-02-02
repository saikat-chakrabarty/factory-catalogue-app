import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from libs.common.settings import settings

logger = logging.getLogger(__name__)

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Attach a unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        response.headers["X-Git-Commit"] = settings.GIT_COMMIT_SHA

        logger.info("Request processed", extra={"request_id": request_id, "process_time": process_time})
        return response

def add_custom_middleware(app):
    app.add_middleware(RequestContextMiddleware)
