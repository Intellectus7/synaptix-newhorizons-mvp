from flask import jsonify, request, g
from functools import wraps
from datetime import datetime
from os import makedirs, path
import json


# =========================================
# BASE RESPONSE SYSTEM
# =========================================

class Message:
    LOG_DIRECTORY = "app_logs"
    LOG_FILE = "server.log"

    def __init__(
        self,
        message,
        msg_type="success",
        status_code=200,
        data=None
    ):
        self.message = message
        self.msg_type = msg_type
        self.status_code = status_code
        self.data = data or {}

    # =====================================
    # LOGGING
    # =====================================

    def log_message(self):
        makedirs(self.LOG_DIRECTORY, exist_ok=True)

        log_path = path.join(
            self.LOG_DIRECTORY,
            self.LOG_FILE
        )

        timestamp = datetime.utcnow().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "type": self.msg_type,
            "message": self.message,
            "status_code": self.status_code
        }

        with open(log_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(log_entry) + "\n")

    # =====================================
    # RESPONSE
    # =====================================

    def to_dict(self):
        payload = {
            "type": self.msg_type,
            "message": self.message,
            "status_code": self.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }

        if self.data:
            payload["data"] = self.data

        return payload

    def send(self):
        self.log_message()
        print(self.to_dict().get('message', ' '))
        return jsonify(self.to_dict()), self.status_code


# =========================================
# ERROR SYSTEM
# =========================================

class Error(Message):
    def __init__(
        self,
        message="Something went wrong.",
        status_code=400,
        data=None
    ):
        super().__init__(
            message=message,
            msg_type="error",
            status_code=status_code,
            data=data
        )


class BadRequestError(Error):
    def __init__(self, message="Bad request."):
        super().__init__(
            message=message,
            status_code=400
        )


class UnauthorizedError(Error):
    def __init__(self, message="Unauthorized."):
        super().__init__(
            message=message,
            status_code=401
        )


class ForbiddenError(Error):
    def __init__(self, message="Forbidden."):
        super().__init__(
            message=message,
            status_code=403
        )


class NotFoundError(Error):
    def __init__(self, message="Resource not found."):
        super().__init__(
            message=message,
            status_code=404
        )


class ValidationError(Error):
    def __init__(self, errors):
        super().__init__(
            message="Validation failed.",
            status_code=422,
            data={"errors": errors}
        )


class InternalServerError(Error):
    def __init__(self, message="Internal server error."):
        super().__init__(
            message=message,
            status_code=500
        )


# =========================================
# SUCCESS RESPONSES
# =========================================

class Success(Message):
    def __init__(
        self,
        message="Success.",
        data=None,
        status_code=200
    ):
        super().__init__(
            message=message,
            msg_type="success",
            status_code=status_code,
            data=data
        )


# =========================================
# REQUEST VALIDATION DECORATOR
# =========================================

def ensure_requirements(required_fields):
    """
    Ensures required JSON fields exist.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if not request.is_json:
                return BadRequestError(
                    "Request must be JSON."
                ).send()

            payload = request.get_json()

            missing_fields = []

            for field in required_fields:
                if field not in payload:
                    missing_fields.append(field)

            if missing_fields:
                return ValidationError({
                    "missing_fields": missing_fields
                }).send()

            g.payload = payload

            return func(*args, **kwargs)

        return wrapper

    return decorator


# =========================================
# OPTIONAL AUTH DECORATOR
# =========================================

def require_api_key(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        api_key = request.headers.get("X-API-KEY")

        if api_key != "super-secret-key":
            return UnauthorizedError(
                "Invalid API key."
            ).send()

        return func(*args, **kwargs)

    return wrapper