# Responses msg
ERR_CODE = {
    "INTERNAL_SERVER_ERROR": "Internal server error",
}

def create_error_response(detail: str, error_code: str):
    return {
        "error_code": detail,
        "error_messages": error_code
    }

