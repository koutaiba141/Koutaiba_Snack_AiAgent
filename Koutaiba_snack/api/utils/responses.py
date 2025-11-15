
from fastapi.responses import JSONResponse
from typing import Any, Optional

def json_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
    success: bool = True,
) -> JSONResponse:
    """
    Creates a unified JSON response for successful API calls.

    Args:
        data: The payload to be included in the response.
        message: A descriptive message about the result.
        status_code: The HTTP status code.
        success: A boolean indicating the success of the operation.

    Returns:
        A FastAPI JSONResponse object.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "message": message,
            "data": data,
        },
    )

def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    data: Any = None,
) -> JSONResponse:
    """
    Creates a unified JSON response for failed API calls.

    Args:
        message: A descriptive error message.
        status_code: The HTTP status code for the error.
        data: Optional additional data about the error.

    Returns:
        A FastAPI JSONResponse object.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": data,
        },
    )

