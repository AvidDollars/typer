from dependency_injector.wiring import Provide, inject
from fastapi import Request, status, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..containers import Container


@inject
async def log_server_errors(
        request: Request,
        call_next,
        logger=Provide[Container.logger]
):
    try:
        response = await call_next(request)
        return response

    except Exception as ex:
        logger.warning(f"exception: {ex}\n", exc_info=True)
        return Response("internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.errors()[0]["type"],
            "message": exc.errors()[0]["msg"]}
    )
