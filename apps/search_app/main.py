from fastapi import FastAPI
from libs.common.settings import settings
from libs.common.logging import configure_logging
from libs.common.middleware import add_custom_middleware
from libs.common.exceptions import register_exception_handlers
from apps.search_app.routes import factories

# Configure logging.
configure_logging(settings.LOG_LEVEL, environment=settings.APP_ENV)

app = FastAPI(title="Factory Search App", version="0.1.0")

# Add middleware and exception handlers.
add_custom_middleware(app)
register_exception_handlers(app)

# Include search routes.
app.include_router(factories.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Factory Search App!"}
