from enum import Enum


class ApiStatusMessage(Enum):
    SUCCESS = "Success"
    FAIL = "Fail"


class ErrorMessage(Enum):
    ACCOUNT_EXISTED = "Account already registered."
    ACCOUNT_NOT_FOUND = "Account not found."
    Permission_Error = "Permission denied or reply not found"

