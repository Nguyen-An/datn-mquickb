from fastapi import HTTPException, status
from .responses_msg import *

# Phản hồi cho 200 OK
ok_response = {
    "description": "Request was successful",
    "content": {
        "application/json": {
            "example": {
                "message": "Success",
                "data": {}
            }
        }
    }
}

# Phản hồi cho 400 Bad Request
bad_request_response = {
    "description": "Invalid request parameters",
    "content": {
        "application/json": {
            "example": {
                "detail": "Bad Request"
            }
        }
    }
}

# Phản hồi cho 404 Not Found
not_found_response = {
    "description": "Item not found",
    "content": {
        "application/json": {
            "example": {
                "detail": "Not Found"
            }
        }
    }
}

# Phản hồi cho 500 Internal Server Error
internal_server_error_response = {
    "description": "Internal server error",
    "content": {
        "application/json": {
            "example": {
                "detail": "Internal Server Error"
            }
        }
    }
}

common_responses = {
    status.HTTP_200_OK: ok_response,
    status.HTTP_400_BAD_REQUEST: bad_request_response,
    status.HTTP_404_NOT_FOUND: not_found_response,
    status.HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_response
}

def OK(data: any = None):
    if data is None:
        return {
            "message": STT_CODE.SUCCESS
        }
    else:
        return {
            "message": STT_CODE.SUCCESS,
            "data": data
        }
    
def return_exception(e):
    e.status_code = getattr(e, 'status_code', 500)

    if e.status_code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    if e.status_code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    if e.status_code == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    if e.status_code == 403:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=STT_CODE.INTERNAL_SERVER_ERROR)
