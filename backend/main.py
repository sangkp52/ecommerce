from fastapi import FastAPI
from application import create_app
from prometheus_fastapi_instrumentator import Instrumentator
from src.routers import api_router, root_router
from src.auth.router import router as auth_router

app = create_app()

# if __name__ == "__main__":
#     app.run()

Instrumentator().instrument(app).expose(app)
# app.include_router(api_router)
# app.include_router(root_router)
# app.include_router(auth_router)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency"
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    REQUEST_LATENCY.observe(duration)

    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)