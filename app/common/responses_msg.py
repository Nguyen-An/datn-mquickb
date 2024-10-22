# Responses msg
STT_CODE = {
    "INTERNAL_SERVER_ERROR": "Server lỗi, vui lòng liên hệ admin!",
    "SUCCESS": "Thành công.",
    "TOKEN_INVALID": "Token không hợp lệ",
    "ITEM_NOT_FOUND": "Không tìm thấy bản ghi"

}

def create_error_response(detail: str, error_code: str):
    return {
        "error_code": detail,
        "error_messages": error_code
    }

