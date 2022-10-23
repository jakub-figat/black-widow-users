from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from mangum import Mangum

from src.data_access.exceptions import AlreadyExists, DoesNotExist
from src.routes.token import token_router
from src.routes.user import user_router
from src.utils.exceptions import ServiceException


app = FastAPI()


app.include_router(user_router, prefix="/users")
app.include_router(token_router, prefix="/tokens")


handler = Mangum(app)


@app.exception_handler(AlreadyExists)
def handle_already_exists_exception(request: Request, exception: AlreadyExists) -> JSONResponse:
    return JSONResponse(content={"detail": str(exception)}, status_code=status.HTTP_400_BAD_REQUEST)


@app.exception_handler(DoesNotExist)
def handle_does_not_exist(request: Request, exception: DoesNotExist) -> JSONResponse:
    return JSONResponse(content={"detail": str(exception)}, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ServiceException)
def handle_service_exception(request: Request, exception: ServiceException) -> JSONResponse:
    return JSONResponse(content={"detail": str(exception)}, status_code=status.HTTP_400_BAD_REQUEST)


# TODO: environment in serverless.yml
