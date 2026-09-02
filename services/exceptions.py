class LessonNotFoundError(Exception):
    pass


class CourseAccessDeniedError(Exception):
    pass


class InvalidMaterialTypeError(Exception):
    pass


class EmptyMaterialError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass


class MissingTokenSubjectError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class UnitNotFoundError(Exception):
    pass


class CourseAlreadyExistsError(Exception):
    pass


class LessonAlreadyExistsError(Exception):
    pass


class EmptyTitleError(Exception):
    pass
