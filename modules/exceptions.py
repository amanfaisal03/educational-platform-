class AppError(Exception):
    pass


class CourseAccessDeniedError(AppError):
    pass


class CourseAlreadyExistsError(AppError):
    pass


class CourseNotFoundError(AppError):
    pass


class EmptyMaterialError(AppError):
    pass


class EmptyTitleError(AppError):
    pass


class ExpiredTokenError(AppError):
    pass


class InvalidCredentialsError(AppError):
    pass


class InvalidMaterialTypeError(AppError):
    pass


class InvalidTokenError(AppError):
    pass


class LessonAlreadyExistsError(AppError):
    pass


class LessonNotFoundError(AppError):
    pass


class MissingTokenSubjectError(AppError):
    pass


class StudentNotFoundError(AppError):
    pass


class UnitNotFoundError(AppError):
    pass


class UserAlreadyExistsError(AppError):
    pass
