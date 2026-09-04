from fastapi import status

# Base Custom Application Exception
class AppException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


# Specific Business Exceptions
class ProjectNotFoundException(AppException):
    def __init__(self, message: str = "Project was not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="PROJECT_NOT_FOUND",
            message=message
        )


class TaskNotFoundException(AppException):
    def __init__(self, message: str = "Task was not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="TASK_NOT_FOUND",
            message=message
        )


class UserNotFoundException(AppException):
    def __init__(self, message: str = "User was not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="USER_NOT_FOUND",
            message=message
        )


class DuplicateMemberException(AppException):
    def __init__(self, message: str = "User is already a member of this project."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE_MEMBER",
            message=message
        )


class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS",
            message=message
        )


class InsufficientPermissionsException(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="INSUFFICIENT_PERMISSIONS",
            message=message
        )


class BadRequestException(AppException):
    def __init__(self, code: str = "BAD_REQUEST", message: str = "Invalid request."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=code,
            message=message
        )
