from application import create_app
from prometheus_fastapi_instrumentator import Instrumentator

app = create_app()

# if __name__ == "__main__":
#     app.run()

app = FastAPI()
Instrumentator().instrument(app).expose(app)