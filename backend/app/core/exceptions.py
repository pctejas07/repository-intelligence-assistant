from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import logger


class RepositoryNotFoundException(Exception):

    def __init__(
        self,
        repository_name: str
    ):
        self.repository_name = repository_name


async def repository_not_found_handler(
    request: Request,
    exc: RepositoryNotFoundException
):

    logger.error(
        f"Repository not found: "
        f"{exc.repository_name}"
    )

    return JSONResponse(
        status_code=404,
        content={
            "message": (
                f"Repository "
                f"'{exc.repository_name}' "
                f"not found"
            )
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(
        "Unhandled exception"
    )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error"
        }
    )