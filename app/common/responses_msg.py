# Responses msg
STT_CODE = {
    "INTERNAL_SERVER_ERROR": "Server lỗi, vui lòng liên hệ admin!",
    "SUCCESS": "Thành công!",
    "TOKEN_INVALID": "Token không hợp lệ!",
    "ITEM_NOT_FOUND": "Không tìm thấy bản ghi!",
    "INVALID_MISSING_TOKEN": "Token không hợp lệ!",
    "PASSWORD_INCORRECT": "Mật khẩu không chính xác!",
    "ORDER_ID_REQUIRED": "order_id là trường bắt buộc",
    "TABLE_NOT_FOUND": "Bàn không tồn tại",
    "TABLE_HAS_BEEN_USED": "Bàn đã được sử dụng",
    "TABLE_NOT_USED": "Bàn chưa được sử dụng",
    "USER_HAS_BOOKED_TABLE": "Người dùng đã đặt bàn",
    "USER_HAS_NOT_BOOKED_TABLE": "Người dùng chưa đặt bàn",
    "USER_HAS_MORE_THAN_ORDER_OR_PENDING_ORDER": "Người dùng đang còn nhiều hơn 1 order hoặc đơn chờ",
    "INCORRECT_LOGIN_TYPE": "Loại đăng nhập không đúng"
}

def create_error_response(detail: str, error_code: str):
    return {
        "error_code": detail,
        "error_messages": error_code
    }

