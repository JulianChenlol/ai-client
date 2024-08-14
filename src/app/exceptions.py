from pydantic.errors import PydanticUserError


class NotFoundError(PydanticUserError):
    code = "not_found"
    message = "{msg}"


class FieldNotFoundError(PydanticUserError):
    code = "not_found.field"
    message = "{msg}"


class ModelNotFoundError(PydanticUserError):
    code = "not_found.model"
    message = "{msg}"


class ExistsError(PydanticUserError):
    code = "exists"
    message = "{msg}"


class InvalidConfigurationError(PydanticUserError):
    code = "invalid.configuration"
    message = "{msg}"


class InvalidFilterError(PydanticUserError):
    code = "invalid.filter"
    message = "{msg}"


class InvalidUsernameError(PydanticUserError):
    code = "invalid.username"
    message = "{msg}"


class InvalidPasswordError(PydanticUserError):
    code = "invalid.password"
    message = "{msg}"
