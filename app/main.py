# Redis
from app.dependencies import redis
# Fastapi
from app.dependencies import fastapi
from app.dependencies import openapi
from app.dependencies import responses
from app.dependencies import exceptions
# CORS
from app.dependencies import cors
# Rate Limiter
from app.dependencies import limiter
# Context
from app.dependencies import plugins, RawContextMiddleware
# from fastapi_limiter.depends import RateLimiter
# Routes
from app.dependencies import router_example
# Settings & Config
from app.dependencies import settings, configuration

app = fastapi.FastAPI(
    redoc_url=f'{configuration.default_api}/redoc',
    docs_url=f'{configuration.default_api}/docs',
    openapi_url=f'{configuration.default_api}/openapi.json',
)
# OpenApi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = openapi.get_openapi(
        title='Files API',
        version='1.0',
        description='API Server For files administration',
        terms_of_service='http://swagger.io/terms/',
        contact= {
            'name': 'API Support',
            'url': 'http://www.swagger.io/support',
            'email': 'support@swagger.io',
        },
        license_info= {
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        },
        tags=[
            {
                'name': 'files',
                'description': 'Files Service',
            },
        ],
        routes=app.routes,
    )
    return openapi_schema
app.openapi = custom_openapi

# CORS
http_client = 'http://' + settings.CLIENT_URL
https_client = 'https://' + settings.CLIENT_URL
origins = [
    http_client,
    https_client,
]
methods = [
    'OPTIONS',
    'GET',
    'POST',
    'PUT',
    'DELETE',
]

# Middleware
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=['*'],
)
app.add_middleware(
    RawContextMiddleware,
    plugins=(
        plugins.request_id.RequestIdPlugin(),
        plugins.correlation_id.CorrelationIdPlugin(),
    ),
)

# Startup
@app.on_event('startup')
async def startup():
    user = settings.REDIS_USER
    password = settings.REDIS_PASSWORD
    host = settings.REDIS_HOST
    port = settings.REDIS_PORT
    redis_client = redis.from_url(f'redis://{user}:{password}@{host}:{port}')
    await limiter.FastAPILimiter.init(redis=redis_client)

# Handlers
@app.exception_handler(exceptions.HTTPException)
def http_exception_handler(request: fastapi.Request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content = {
            'success': False,
            'message': exc.detail,
        }
    )

# Routes
app.include_router(router_example)
